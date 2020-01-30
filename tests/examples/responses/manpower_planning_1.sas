proc optmodel;
   var numWorkers {{'unskilled','semiskilled','skilled'}, {0,1,2,3}} >= 0;
   numWorkers['unskilled', 0].lb = 2000;
   numWorkers['unskilled', 0].ub = 2000;
   numWorkers['semiskilled', 0].lb = 1500;
   numWorkers['semiskilled', 0].ub = 1500;
   numWorkers['skilled', 0].lb = 1000;
   numWorkers['skilled', 0].ub = 1000;
   var numRecruits {{'unskilled','semiskilled','skilled'}, {1,2,3}} >= 0;
   numRecruits['unskilled', 1].ub = 500;
   numRecruits['unskilled', 2].ub = 500;
   numRecruits['unskilled', 3].ub = 500;
   numRecruits['semiskilled', 1].ub = 800;
   numRecruits['semiskilled', 2].ub = 800;
   numRecruits['semiskilled', 3].ub = 800;
   numRecruits['skilled', 1].ub = 500;
   numRecruits['skilled', 2].ub = 500;
   numRecruits['skilled', 3].ub = 500;
   var numRedundant {{'unskilled','semiskilled','skilled'}, {1,2,3}} >= 0;
   var numShortTime {{'unskilled','semiskilled','skilled'}, {1,2,3}} >= 0 <= 50;
   var numExcess {{'unskilled','semiskilled','skilled'}, {1,2,3}} >= 0;
   var numRetrain {{<'unskilled','semiskilled'>,<'semiskilled','skilled'>}, {1,2,3}} >= 0;
   numRetrain['unskilled', 'semiskilled', 1].ub = 200.0;
   numRetrain['unskilled', 'semiskilled', 2].ub = 200.0;
   numRetrain['unskilled', 'semiskilled', 3].ub = 200.0;
   var numDowngrade {{<'semiskilled','unskilled'>,<'skilled','semiskilled'>,<'skilled','unskilled'>}, {1,2,3}} >= 0;
   con demand_unskilled_1 : numWorkers['unskilled', 1] - 0.5 * numShortTime['unskilled', 1] - numExcess['unskilled', 1] = 1000.0;
   con demand_unskilled_2 : numWorkers['unskilled', 2] - 0.5 * numShortTime['unskilled', 2] - numExcess['unskilled', 2] = 500.0;
   con demand_unskilled_3 : numWorkers['unskilled', 3] - 0.5 * numShortTime['unskilled', 3] - numExcess['unskilled', 3] = 0.0;
   con demand_semiskilled_1 : numWorkers['semiskilled', 1] - 0.5 * numShortTime['semiskilled', 1] - numExcess['semiskilled', 1] = 1400.0;
   con demand_semiskilled_2 : numWorkers['semiskilled', 2] - 0.5 * numShortTime['semiskilled', 2] - numExcess['semiskilled', 2] = 2000.0;
   con demand_semiskilled_3 : numWorkers['semiskilled', 3] - 0.5 * numShortTime['semiskilled', 3] - numExcess['semiskilled', 3] = 2500.0;
   con demand_skilled_1 : numWorkers['skilled', 1] - 0.5 * numShortTime['skilled', 1] - numExcess['skilled', 1] = 1000.0;
   con demand_skilled_2 : numWorkers['skilled', 2] - 0.5 * numShortTime['skilled', 2] - numExcess['skilled', 2] = 1500.0;
   con demand_skilled_3 : numWorkers['skilled', 3] - 0.5 * numShortTime['skilled', 3] - numExcess['skilled', 3] = 2000.0;
   con flow_balance_unskilled_1 : numWorkers['unskilled', 1] - 0.9 * numWorkers['unskilled', 0] - 0.75 * numRecruits['unskilled', 1] - 0.5 * numDowngrade['semiskilled', 'unskilled', 1] - 0.5 * numDowngrade['skilled', 'unskilled', 1] + numRetrain['unskilled', 'semiskilled', 1] + numRedundant['unskilled', 1] = 0.0;
   con flow_balance_unskilled_2 : numWorkers['unskilled', 2] - 0.9 * numWorkers['unskilled', 1] - 0.75 * numRecruits['unskilled', 2] - 0.5 * numDowngrade['semiskilled', 'unskilled', 2] - 0.5 * numDowngrade['skilled', 'unskilled', 2] + numRetrain['unskilled', 'semiskilled', 2] + numRedundant['unskilled', 2] = 0.0;
   con flow_balance_unskilled_3 : numWorkers['unskilled', 3] - 0.9 * numWorkers['unskilled', 2] - 0.75 * numRecruits['unskilled', 3] - 0.5 * numDowngrade['semiskilled', 'unskilled', 3] - 0.5 * numDowngrade['skilled', 'unskilled', 3] + numRetrain['unskilled', 'semiskilled', 3] + numRedundant['unskilled', 3] = 0.0;
   con flow_balance_semiskilled_1 : numWorkers['semiskilled', 1] - 0.95 * numWorkers['semiskilled', 0] - 0.8 * numRecruits['semiskilled', 1] - 0.95 * numRetrain['unskilled', 'semiskilled', 1] - 0.5 * numDowngrade['skilled', 'semiskilled', 1] + numRetrain['semiskilled', 'skilled', 1] + numDowngrade['semiskilled', 'unskilled', 1] + numRedundant['semiskilled', 1] = 0.0;
   con flow_balance_semiskilled_2 : numWorkers['semiskilled', 2] - 0.95 * numWorkers['semiskilled', 1] - 0.8 * numRecruits['semiskilled', 2] - 0.95 * numRetrain['unskilled', 'semiskilled', 2] - 0.5 * numDowngrade['skilled', 'semiskilled', 2] + numRetrain['semiskilled', 'skilled', 2] + numDowngrade['semiskilled', 'unskilled', 2] + numRedundant['semiskilled', 2] = 0.0;
   con flow_balance_semiskilled_3 : numWorkers['semiskilled', 3] - 0.95 * numWorkers['semiskilled', 2] - 0.8 * numRecruits['semiskilled', 3] - 0.95 * numRetrain['unskilled', 'semiskilled', 3] - 0.5 * numDowngrade['skilled', 'semiskilled', 3] + numRetrain['semiskilled', 'skilled', 3] + numDowngrade['semiskilled', 'unskilled', 3] + numRedundant['semiskilled', 3] = 0.0;
   con flow_balance_skilled_1 : numWorkers['skilled', 1] - 0.95 * numWorkers['skilled', 0] - 0.9 * numRecruits['skilled', 1] - 0.95 * numRetrain['semiskilled', 'skilled', 1] + numDowngrade['skilled', 'unskilled', 1] + numDowngrade['skilled', 'semiskilled', 1] + numRedundant['skilled', 1] = 0.0;
   con flow_balance_skilled_2 : numWorkers['skilled', 2] - 0.95 * numWorkers['skilled', 1] - 0.9 * numRecruits['skilled', 2] - 0.95 * numRetrain['semiskilled', 'skilled', 2] + numDowngrade['skilled', 'unskilled', 2] + numDowngrade['skilled', 'semiskilled', 2] + numRedundant['skilled', 2] = 0.0;
   con flow_balance_skilled_3 : numWorkers['skilled', 3] - 0.95 * numWorkers['skilled', 2] - 0.9 * numRecruits['skilled', 3] - 0.95 * numRetrain['semiskilled', 'skilled', 3] + numDowngrade['skilled', 'unskilled', 3] + numDowngrade['skilled', 'semiskilled', 3] + numRedundant['skilled', 3] = 0.0;
   con semiskill_retrain_1 : numRetrain['semiskilled', 'skilled', 1] - 0.25 * numWorkers['skilled', 1] <= 0.0;
   con semiskill_retrain_2 : numRetrain['semiskilled', 'skilled', 2] - 0.25 * numWorkers['skilled', 2] <= 0.0;
   con semiskill_retrain_3 : numRetrain['semiskilled', 'skilled', 3] - 0.25 * numWorkers['skilled', 3] <= 0.0;
   con overmanning_1 : numExcess['unskilled', 1] + numExcess['semiskilled', 1] + numExcess['skilled', 1] <= 150;
   con overmanning_2 : numExcess['unskilled', 2] + numExcess['semiskilled', 2] + numExcess['skilled', 2] <= 150;
   con overmanning_3 : numExcess['unskilled', 3] + numExcess['semiskilled', 3] + numExcess['skilled', 3] <= 150;
   min cost_obj = 200 * numRedundant['unskilled', 1] + 500 * numShortTime['unskilled', 1] + 1500 * numExcess['unskilled', 1] + 200 * numRedundant['unskilled', 2] + 500 * numShortTime['unskilled', 2] + 1500 * numExcess['unskilled', 2] + 200 * numRedundant['unskilled', 3] + 500 * numShortTime['unskilled', 3] + 1500 * numExcess['unskilled', 3] + 500 * numRedundant['semiskilled', 1] + 400 * numShortTime['semiskilled', 1] + 2000 * numExcess['semiskilled', 1] + 500 * numRedundant['semiskilled', 2] + 400 * numShortTime['semiskilled', 2] + 2000 * numExcess['semiskilled', 2] + 500 * numRedundant['semiskilled', 3] + 400 * numShortTime['semiskilled', 3] + 2000 * numExcess['semiskilled', 3] + 500 * numRedundant['skilled', 1] + 400 * numShortTime['skilled', 1] + 3000 * numExcess['skilled', 1] + 500 * numRedundant['skilled', 2] + 400 * numShortTime['skilled', 2] + 3000 * numExcess['skilled', 2] + 500 * numRedundant['skilled', 3] + 400 * numShortTime['skilled', 3] + 3000 * numExcess['skilled', 3] + 400.0 * numRetrain['unskilled', 'semiskilled', 1] + 400.0 * numRetrain['unskilled', 'semiskilled', 2] + 400.0 * numRetrain['unskilled', 'semiskilled', 3] + 500.0 * numRetrain['semiskilled', 'skilled', 1] + 500.0 * numRetrain['semiskilled', 'skilled', 2] + 500.0 * numRetrain['semiskilled', 'skilled', 3];
   solve;
quit;