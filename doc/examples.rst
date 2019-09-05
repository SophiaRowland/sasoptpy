
.. _examples:

Examples
********

Examples are provided from `SAS/OR documentation <http://go.documentation.sas.com/?docsetId=ormpex&docsetTarget=titlepage.htm&docsetVersion=14.3&locale=en>`_.

.. ipython:: python
   :suppress:
   
   hostname = os.getenv('CASHOST')
   port = os.getenv('CASPORT')
   from swat import CAS
   cas_conn = CAS(hostname, port)

Viya Examples / Concrete
------------------------

.. toctree::
   :maxdepth: 1

   Food Manufacture 1 <examples/food_manufacture_1.rst>
   Food Manufacture 2 <examples/food_manufacture_2.rst>
   Factory Planning 1 <examples/factory_planning_1.rst>
   Factory Planning 2 <examples/factory_planning_2.rst>
   Manpower Planning <examples/manpower_planning.rst>
   Refinery Optimization <examples/refinery_optimization.rst>
   Mining Optimization <examples/mining_optimization.rst>
   Farm Planning <examples/farm_planning.rst>
   Economic Planning <examples/economic_planning.rst>
   Decentralization <examples/decentralization.rst>
   SAS/OR Blog: Optimal Wedding <examples/optimal_wedding.rst>
   SAS/OR Blog: Kidney Exchange <examples/kidney_exchange.rst>
   Multiobjective <examples/multiobjective.rst>
   Least Squares <examples/least_squares.rst>

Viya Examples / Abstract
------------------------

.. toctree::
   :maxdepth: 1
   
   Curve Fitting <examples/curve_fitting.rst>
   Nonlinear 1 <examples/nonlinear_1.rst>
   Nonlinear 2 <examples/nonlinear_2.rst>

SAS (saspy) Examples
--------------------

.. toctree::
   :maxdepth: 1

   Decentralization <examples/decentralization_saspy.rst>

RESTful API Examples
--------------------

.. toctree::
   :maxdepth: 1
   
   Knapsack <examples/knapsack.rst>
