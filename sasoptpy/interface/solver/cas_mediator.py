# CAS (SAS Viya) interface for sasoptpy

import inspect

import pandas as pd
import numpy as np

import sasoptpy
from sasoptpy.interface import Mediator

class CASMediator(Mediator):

    def __init__(self, caller, cas_session):
        if cas_session is None:
            raise RuntimeError('CAS Session is not available')
        self.caller = caller
        self.session = cas_session

    def solve(self, **kwargs):
        """
        Solve action for single models
        """
        self.session.loadactionset(actionset='optimization')

        mps = kwargs.get('mps', kwargs.get('frame', False))
        options = kwargs.get('options', dict())

        mps_indicator = self.is_mps_format_needed(mps, options)

        if mps_indicator:
            return self.solve_with_mps(**kwargs)
        else:
            return self.solve_with_optmodel(**kwargs)

    def submit(self, **kwargs):
        """
        Submit action for custom input and workspaces
        """
        self.session.loadactionset(actionset='optimization')
        return self.submit_optmodel_code(**kwargs)


    def is_mps_format_needed(self, mps_option, options):

        enforced = False
        mps_option = mps_option
        session = self.session
        caller = self.caller

        if not isinstance(caller, sasoptpy.Model):
            return False

        model = caller

        # If runOptmodel action is not available on server
        if not hasattr(session.optimization, 'runoptmodel'):
            mps_option = True
            enforced = True

        if 'decomp' in options:
            mps_option = True
            enforced = True

        if mps_option:
            switch = False
            # Sets and parameter belong to abstract models
            if model.get_sets() or model.get_parameters():
                print('INFO: Model {} has data on server,'.format(model.get_name()),
                      'switching to OPTMODEL mode.')
                switch = True
            # MPS format cannot represent nonlinear problems
            elif not sasoptpy.is_linear(model):
                print('INFO: Model {} includes nonlinear or abstract'.format(
                    model.get_name()),
                      'components, switching to OPTMODEL mode.')
                switch = True

            if switch and enforced and mps_option:
                raise RuntimeError('Problem requires runOptmodel action which '
                                   'is not available or appropriate')
            elif switch:
                mps_option = False

        return mps_option

    def solve_with_mps(self, **kwargs):

        model = self.caller
        session = self.session
        verbose = kwargs.get('verbose', False)
        submit = kwargs.get('submit', True)
        options = kwargs.get('options', dict())
        primalin = kwargs.get('primalin', False)
        name = kwargs.get('name', None)
        replace = kwargs.get('replace', True)
        drop = kwargs.get('drop', False)

        print('NOTE: Converting model {} to DataFrame.'.format(model._name))
        # Pre-upload argument parse

        # Find problem type and initial values
        ptype = 1  # LP
        for v in model._variables:
            if v._type != sasoptpy.CONT:
                ptype = 2
                break

        # Decomp check
        try:
            if options['decomp']['method'] == 'user':
                        user_blocks = self.upload_user_blocks()
                        options['decomp'] = {'blocks': user_blocks}
        except KeyError:
            pass

        # Initial value check for MIP
        if primalin:
            init_values = []
            var_names = []
            if ptype == 2:
                for v in model._variables:
                    if v._init is not None:
                        var_names.append(v._name)
                        init_values.append(v._init)
                if (len(init_values) > 0 and
                   options.get('primalin', 1) is not None):
                    primalinTable = pd.DataFrame(
                        data={'_VAR_': var_names, '_VALUE_': init_values})
                    session.upload_frame(
                        primalinTable, casout={
                            'name': 'PRIMALINTABLE', 'replace': True})
                    options['primalin'] = 'PRIMALINTABLE'

        # Check if objective constant workaround is needed
        sfunc = session.solveLp if ptype == 1 else session.solveMilp
        has_arg = 'objconstant' in inspect.signature(sfunc).parameters
        if has_arg and 'objconstant' not in options:
            objconstant = model.get_objective()._linCoef['CONST']['val']
            options['objconstant'] = objconstant

        # Upload the problem
        mps_table = self.upload_model(name, replace=replace,
                                      constant=not has_arg, verbose=verbose)

        if ptype == 1:
            valid_opts = inspect.signature(session.solveLp).parameters
            lp_opts = {}
            for key, value in options.items():
                if key in valid_opts:
                    lp_opts[key] = value
            response = session.solveLp(
                data=mps_table.name, **lp_opts,
                primalOut={'caslib': 'CASUSER', 'name': 'primal',
                           'replace': True},
                dualOut={'caslib': 'CASUSER', 'name': 'dual',
                         'replace': True},
                objSense=model.get_objective().get_sense())
        elif ptype == 2:
            valid_opts = inspect.signature(session.solveMilp).parameters
            milp_opts = {}
            for key, value in options.items():
                if key in valid_opts:
                    milp_opts[key] = value
            response = session.solveMilp(
                data=mps_table.name, **milp_opts,
                primalOut={'caslib': 'CASUSER', 'name': 'primal',
                           'replace': True},
                dualOut={'caslib': 'CASUSER', 'name': 'dual',
                         'replace': True},
                objSense=model.get_objective().get_sense())

        model.response = response

        # Parse solution
        if(response.get_tables('status')[0] == 'OK'):
            model._primalSolution = session.CASTable(
                'primal', caslib='CASUSER').to_frame()
            model._dualSolution = session.CASTable(
                'dual', caslib='CASUSER').to_frame()
            # Bring solution to variables
            for _, row in model._primalSolution.iterrows():
                if ('_SOL_' in model._primalSolution and row['_SOL_'] == 1)\
                     or '_SOL_' not in model._primalSolution:
                    model._variableDict[row['_VAR_']]._value =\
                        row['_VALUE_']

            # Capturing dual values for LP problems
            if ptype == 1:
                model._primalSolution = model._primalSolution[
                    ['_VAR_', '_LBOUND_', '_UBOUND_', '_VALUE_',
                     '_R_COST_']]
                model._primalSolution.columns = ['var', 'lb', 'ub',
                                                'value', 'rc']
                model._dualSolution = model._dualSolution[
                    ['_ROW_', '_ACTIVITY_', '_VALUE_']]
                model._dualSolution.columns = ['con', 'value', 'dual']
                for _, row in model._primalSolution.iterrows():
                    model._variableDict[row['var']]._dual = row['rc']
                for _, row in model._dualSolution.iterrows():
                    model._constraintDict[row['con']]._dual = row['dual']
            elif ptype == 2:
                try:
                    model._primalSolution = model._primalSolution[
                        ['_VAR_', '_LBOUND_', '_UBOUND_', '_VALUE_',
                         '_SOL_']]
                    model._primalSolution.columns = ['var', 'lb', 'ub',
                                                    'value', 'solution']
                    model._dualSolution = model._dualSolution[
                        ['_ROW_', '_ACTIVITY_', '_SOL_']]
                    model._dualSolution.columns = ['con', 'value',
                                                  'solution']
                except:
                    model._primalSolution = model._primalSolution[
                        ['_VAR_', '_LBOUND_', '_UBOUND_', '_VALUE_']]
                    model._primalSolution.columns = ['var', 'lb', 'ub',
                                                    'value']
                    model._dualSolution = model._dualSolution[
                        ['_ROW_', '_ACTIVITY_']]
                    model._dualSolution.columns = ['con', 'value']

        # Drop tables
        if drop:
            session.table.droptable(table=mps_table.name)
            if user_blocks is not None:
                session.table.droptable(table=user_blocks)
            if primalin:
                session.table.droptable(table='PRIMALINTABLE')

        # Post-solve parse
        if(response.get_tables('status')[0] == 'OK'):
            # Print problem and solution summaries
            model._problemSummary = response.ProblemSummary[['Label1',
                                                            'cValue1']]
            model._solutionSummary = response.SolutionSummary[['Label1',
                                                              'cValue1']]
            model._problemSummary.set_index(['Label1'], inplace=True)
            model._problemSummary.columns = ['Value']
            model._problemSummary.index.names = ['Label']
            model._solutionSummary.set_index(['Label1'], inplace=True)
            model._solutionSummary.columns = ['Value']
            model._solutionSummary.index.names = ['Label']
            # Record status and time
            model._status = response.solutionStatus
            model._soltime = response.solutionTime
            if('OPTIMAL' in response.solutionStatus):
                model._objval = response.objective
                # Replace initial values with current values
                for v in model._variables:
                    v._init = v._value
                return model._primalSolution
            else:
                print('NOTE: Response {}'.format(response.solutionStatus))
                model._objval = 0
                return None
        else:
            print('ERROR: {}'.format(response.get_tables('status')[0]))
            return None

    def solve_with_optmodel(self, **kwargs):

        model = self.caller
        session = self.session
        verbose = kwargs.get('verbose', False)
        submit = kwargs.get('submit', True)

        print('NOTE: Converting model {} to OPTMODEL.'.format(model._name))
        options = kwargs.get('options', dict())
        primalin = kwargs.get('primalin', False)
        optmodel_string = model.to_optmodel(header=False, options=options,
                                           ods=False, primalin=primalin,
                                            parse=True)
        if verbose:
            print(optmodel_string)
        if not submit:
            return optmodel_string
        print('NOTE: Submitting OPTMODEL code to CAS server.')
        response = session.runOptmodel(
            optmodel_string,
            outputTables={
                'names': {'solutionSummary': 'solutionSummary',
                          'problemSummary': 'problemSummary'}
                }
            )

        model.response = response

        # Parse solution
        return self.parse_cas_solution()

        if('OPTIMAL' in response.solutionStatus or 'ABSFCONV' in response.solutionStatus or
           'BEST_FEASIBLE' in response.solutionStatus):
            model._objval = response.objective
            # Replace initial values with current values
            for v in model._variables:
                v._init = v._value
            return model._primalSolution
        else:
            print('NOTE: Response {}'.format(response.solutionStatus))
            model._objval = 0
            return None


    def parse_cas_solution(self):
        caller = self.caller
        session = self.session
        response = caller.response

        solution = session.CASTable('solution').to_frame()
        dual_solution = session.CASTable('dual').to_frame()

        caller._primalSolution = solution
        caller._dualSolution = dual_solution

        caller._problemSummary = self.parse_optmodel_table('problemSummary')
        caller._solutionSummary = self.parse_optmodel_table('solutionSummary')

        caller._status = response.solutionStatus
        caller._soltime = response.solutionTime

        self.set_variable_values(solution)
        self.set_constraint_values(dual_solution)

        self.set_model_objective_value()
        self.set_variable_init_values()

        return solution

    def parse_optmodel_table(self, table):
        session = self.session
        parsed_df = session.CASTable(table).to_frame()[['Label1', 'cValue1']]
        parsed_df.columns = ['Label', 'Value']
        parsed_df = parsed_df.set_index(['Label'])
        return parsed_df

    def set_variable_values(self, solution):
        caller = self.caller
        solver = caller.get_solution_summary().loc['Solver', 'Value']
        for _, row in solution.iterrows():
            caller.set_variable_value(row['var'], row['value'])
            if solver == 'LP':
                caller.set_dual_value(row['var'], row['rc'])

    def set_constraint_values(self, solution):
        caller = self.caller
        solver = caller.get_solution_summary().loc['Solver', 'Value']
        if solver == 'LP':
            for _, row in solution.iterrows():
                con = caller.get_constraint(row['con'])
                if con is not None:
                    con.set_dual(row['dual'])

    def set_model_objective_value(self):
        caller = self.caller
        if not sasoptpy.core.util.is_model(caller):
            return
        objval = caller.response.objective
        caller.set_objective_value(objval)

    def set_variable_init_values(self):
        caller = self.caller
        if not sasoptpy.core.util.is_model(caller):
            return
        for v in caller.get_variables():
            v.set_init(v.get_value())

    def upload_user_blocks(self):
        """
        Uploads user-defined decomposition blocks to the CAS server

        Returns
        -------
        name : string
            CAS table name of the user-defined decomposition blocks

        Examples
        --------

        >>> userblocks = m.upload_user_blocks()
        >>> m.solve(milp={'decomp': {'blocks': userblocks}})

        """
        sess = self.session
        model = self.caller

        blocks_dict = {}
        block_counter = 0
        decomp_table = []
        for c in model._constraints:
            if c._block is not None:
                if c._block not in blocks_dict:
                    blocks_dict[c._block] = block_counter
                    block_counter += 1
                block_no = blocks_dict[c._block]
                decomp_table.append([c.get_name(), block_no])
        frame_decomp_table = pd.DataFrame(decomp_table,
                                          columns=['_ROW_', '_BLOCK_'])
        response = sess.upload_frame(frame_decomp_table,
                                     casout={'name': 'BLOCKSTABLE',
                                             'replace': True})
        return(response.name)

    def upload_model(self, name=None, replace=True, constant=False,
                     verbose=False):
        """
        Converts internal model to MPS table and upload to CAS session

        Parameters
        ----------
        name : string, optional
            Desired name of the MPS table on the server
        replace : boolean, optional
            Option to replace the existing MPS table

        Returns
        -------
        frame : :class:`swat.cas.table.CASTable`
            Reference to the uploaded CAS Table

        Notes
        -----

        - This method returns None if the model session is not valid.
        - Name of the table is randomly assigned if name argument is None
          or not given.
        - This method should not be used if :func:`Model.solve` is going
          to be used. :func:`Model.solve` calls this method internally.

        """
        model = self.caller
        df = model.to_mps(constant=constant)
        if verbose:
            print(df.to_string())

        print('NOTE: Uploading the problem DataFrame to the server.')
        if name is not None:
            return self.session.upload_frame(
                data=df, casout={'name': name, 'replace': replace})
        else:
            return self.session.upload_frame(
                data=df, casout={'replace': replace})


    def submit_optmodel_code(self, **kwargs):

        caller = self.caller
        session = self.session
        optmodel_code = sasoptpy.util.to_optmodel(caller, header=False, parse=True)
        verbose = kwargs.get('verbose', None)

        if verbose:
            print(optmodel_code)

        response = session.runOptmodel(
            optmodel_code,
            outputTables={
                'names': {'solutionSummary': 'solutionSummary',
                          'problemSummary': 'problemSummary',
                          'Print1.PrintTable': 'primal',
                          'Print2.PrintTable': 'dual'}
            }
        )

        if response['status'] == 'OK':

            for row in response['Print1.PrintTable']:
                original_name = row['var'].split('[')[0]
                print(locals().get(original_name))
                print(globals().get(original_name))
