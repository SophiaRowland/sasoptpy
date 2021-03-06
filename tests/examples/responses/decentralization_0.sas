proc optmodel;
   var assign {{'A','B','C','D','E'}, {'Bristol','Brighton','London'}} binary;
   var product {{<'A','Bristol','B','Bristol'>,<'A','Bristol','B','Brighton'>,<'A','Bristol','B','London'>,<'A','Bristol','C','Bristol'>,<'A','Bristol','C','Brighton'>,<'A','Bristol','C','London'>,<'A','Bristol','D','Bristol'>,<'A','Bristol','D','Brighton'>,<'A','Bristol','D','London'>,<'A','Bristol','E','Bristol'>,<'A','Bristol','E','Brighton'>,<'A','Bristol','E','London'>,<'A','Brighton','B','Bristol'>,<'A','Brighton','B','Brighton'>,<'A','Brighton','B','London'>,<'A','Brighton','C','Bristol'>,<'A','Brighton','C','Brighton'>,<'A','Brighton','C','London'>,<'A','Brighton','D','Bristol'>,<'A','Brighton','D','Brighton'>,<'A','Brighton','D','London'>,<'A','Brighton','E','Bristol'>,<'A','Brighton','E','Brighton'>,<'A','Brighton','E','London'>,<'A','London','B','Bristol'>,<'A','London','B','Brighton'>,<'A','London','B','London'>,<'A','London','C','Bristol'>,<'A','London','C','Brighton'>,<'A','London','C','London'>,<'A','London','D','Bristol'>,<'A','London','D','Brighton'>,<'A','London','D','London'>,<'A','London','E','Bristol'>,<'A','London','E','Brighton'>,<'A','London','E','London'>,<'B','Bristol','C','Bristol'>,<'B','Bristol','C','Brighton'>,<'B','Bristol','C','London'>,<'B','Bristol','D','Bristol'>,<'B','Bristol','D','Brighton'>,<'B','Bristol','D','London'>,<'B','Bristol','E','Bristol'>,<'B','Bristol','E','Brighton'>,<'B','Bristol','E','London'>,<'B','Brighton','C','Bristol'>,<'B','Brighton','C','Brighton'>,<'B','Brighton','C','London'>,<'B','Brighton','D','Bristol'>,<'B','Brighton','D','Brighton'>,<'B','Brighton','D','London'>,<'B','Brighton','E','Bristol'>,<'B','Brighton','E','Brighton'>,<'B','Brighton','E','London'>,<'B','London','C','Bristol'>,<'B','London','C','Brighton'>,<'B','London','C','London'>,<'B','London','D','Bristol'>,<'B','London','D','Brighton'>,<'B','London','D','London'>,<'B','London','E','Bristol'>,<'B','London','E','Brighton'>,<'B','London','E','London'>,<'C','Bristol','D','Bristol'>,<'C','Bristol','D','Brighton'>,<'C','Bristol','D','London'>,<'C','Bristol','E','Bristol'>,<'C','Bristol','E','Brighton'>,<'C','Bristol','E','London'>,<'C','Brighton','D','Bristol'>,<'C','Brighton','D','Brighton'>,<'C','Brighton','D','London'>,<'C','Brighton','E','Bristol'>,<'C','Brighton','E','Brighton'>,<'C','Brighton','E','London'>,<'C','London','D','Bristol'>,<'C','London','D','Brighton'>,<'C','London','D','London'>,<'C','London','E','Bristol'>,<'C','London','E','Brighton'>,<'C','London','E','London'>,<'D','Bristol','E','Bristol'>,<'D','Bristol','E','Brighton'>,<'D','Bristol','E','London'>,<'D','Brighton','E','Bristol'>,<'D','Brighton','E','Brighton'>,<'D','Brighton','E','London'>,<'D','London','E','Bristol'>,<'D','London','E','Brighton'>,<'D','London','E','London'>}} binary;
   max netBenefit = 10 * assign['A', 'Bristol'] + 10 * assign['A', 'Brighton'] + 15 * assign['B', 'Bristol'] + 20 * assign['B', 'Brighton'] + 10 * assign['C', 'Bristol'] + 15 * assign['C', 'Brighton'] + 20 * assign['D', 'Bristol'] + 15 * assign['D', 'Brighton'] + 5 * assign['E', 'Bristol'] + 15 * assign['E', 'Brighton'] - 5.0 * product['A', 'Bristol', 'C', 'Bristol'] - 14.0 * product['A', 'Bristol', 'C', 'Brighton'] - 13.0 * product['A', 'Bristol', 'C', 'London'] - 7.5 * product['A', 'Bristol', 'D', 'Bristol'] - 21.0 * product['A', 'Bristol', 'D', 'Brighton'] - 19.5 * product['A', 'Bristol', 'D', 'London'] - 14.0 * product['A', 'Brighton', 'C', 'Bristol'] - 5.0 * product['A', 'Brighton', 'C', 'Brighton'] - 9.0 * product['A', 'Brighton', 'C', 'London'] - 21.0 * product['A', 'Brighton', 'D', 'Bristol'] - 7.5 * product['A', 'Brighton', 'D', 'Brighton'] - 13.5 * product['A', 'Brighton', 'D', 'London'] - 13.0 * product['A', 'London', 'C', 'Bristol'] - 9.0 * product['A', 'London', 'C', 'Brighton'] - 10.0 * product['A', 'London', 'C', 'London'] - 19.5 * product['A', 'London', 'D', 'Bristol'] - 13.5 * product['A', 'London', 'D', 'Brighton'] - 15.0 * product['A', 'London', 'D', 'London'] - 7.0 * product['B', 'Bristol', 'C', 'Bristol'] - 19.6 * product['B', 'Bristol', 'C', 'Brighton'] - 18.2 * product['B', 'Bristol', 'C', 'London'] - 6.0 * product['B', 'Bristol', 'D', 'Bristol'] - 16.8 * product['B', 'Bristol', 'D', 'Brighton'] - 15.6 * product['B', 'Bristol', 'D', 'London'] - 19.6 * product['B', 'Brighton', 'C', 'Bristol'] - 7.0 * product['B', 'Brighton', 'C', 'Brighton'] - 12.6 * product['B', 'Brighton', 'C', 'London'] - 16.8 * product['B', 'Brighton', 'D', 'Bristol'] - 6.0 * product['B', 'Brighton', 'D', 'Brighton'] - 10.8 * product['B', 'Brighton', 'D', 'London'] - 18.2 * product['B', 'London', 'C', 'Bristol'] - 12.6 * product['B', 'London', 'C', 'Brighton'] - 14.0 * product['B', 'London', 'C', 'London'] - 15.6 * product['B', 'London', 'D', 'Bristol'] - 10.8 * product['B', 'London', 'D', 'Brighton'] - 12.0 * product['B', 'London', 'D', 'London'] - 10.0 * product['C', 'Bristol', 'E', 'Bristol'] - 28.0 * product['C', 'Bristol', 'E', 'Brighton'] - 26.0 * product['C', 'Bristol', 'E', 'London'] - 28.0 * product['C', 'Brighton', 'E', 'Bristol'] - 10.0 * product['C', 'Brighton', 'E', 'Brighton'] - 18.0 * product['C', 'Brighton', 'E', 'London'] - 26.0 * product['C', 'London', 'E', 'Bristol'] - 18.0 * product['C', 'London', 'E', 'Brighton'] - 20.0 * product['C', 'London', 'E', 'London'] - 3.5 * product['D', 'Bristol', 'E', 'Bristol'] - 9.8 * product['D', 'Bristol', 'E', 'Brighton'] - 9.1 * product['D', 'Bristol', 'E', 'London'] - 9.8 * product['D', 'Brighton', 'E', 'Bristol'] - 3.5 * product['D', 'Brighton', 'E', 'Brighton'] - 6.3 * product['D', 'Brighton', 'E', 'London'] - 9.1 * product['D', 'London', 'E', 'Bristol'] - 6.3 * product['D', 'London', 'E', 'Brighton'] - 7.0 * product['D', 'London', 'E', 'London'];
   con assign_dept_A : assign['A', 'Bristol'] + assign['A', 'Brighton'] + assign['A', 'London'] = 1;
   con assign_dept_B : assign['B', 'Bristol'] + assign['B', 'Brighton'] + assign['B', 'London'] = 1;
   con assign_dept_C : assign['C', 'Bristol'] + assign['C', 'Brighton'] + assign['C', 'London'] = 1;
   con assign_dept_D : assign['D', 'Bristol'] + assign['D', 'Brighton'] + assign['D', 'London'] = 1;
   con assign_dept_E : assign['E', 'Bristol'] + assign['E', 'Brighton'] + assign['E', 'London'] = 1;
   con cardinality_Bristol : assign['A', 'Bristol'] + assign['B', 'Bristol'] + assign['C', 'Bristol'] + assign['D', 'Bristol'] + assign['E', 'Bristol'] <= 3;
   con cardinality_Brighton : assign['A', 'Brighton'] + assign['B', 'Brighton'] + assign['C', 'Brighton'] + assign['D', 'Brighton'] + assign['E', 'Brighton'] <= 3;
   con cardinality_London : assign['A', 'London'] + assign['B', 'London'] + assign['C', 'London'] + assign['D', 'London'] + assign['E', 'London'] <= 3;
   con pd1_A_Bristol_B_Bristol : product['A', 'Bristol', 'B', 'Bristol'] - assign['A', 'Bristol'] - assign['B', 'Bristol'] >= -1;
   con pd1_A_Bristol_B_Brighton : product['A', 'Bristol', 'B', 'Brighton'] - assign['A', 'Bristol'] - assign['B', 'Brighton'] >= -1;
   con pd1_A_Bristol_B_London : product['A', 'Bristol', 'B', 'London'] - assign['A', 'Bristol'] - assign['B', 'London'] >= -1;
   con pd1_A_Bristol_C_Bristol : product['A', 'Bristol', 'C', 'Bristol'] - assign['A', 'Bristol'] - assign['C', 'Bristol'] >= -1;
   con pd1_A_Bristol_C_Brighton : product['A', 'Bristol', 'C', 'Brighton'] - assign['A', 'Bristol'] - assign['C', 'Brighton'] >= -1;
   con pd1_A_Bristol_C_London : product['A', 'Bristol', 'C', 'London'] - assign['A', 'Bristol'] - assign['C', 'London'] >= -1;
   con pd1_A_Bristol_D_Bristol : product['A', 'Bristol', 'D', 'Bristol'] - assign['A', 'Bristol'] - assign['D', 'Bristol'] >= -1;
   con pd1_A_Bristol_D_Brighton : product['A', 'Bristol', 'D', 'Brighton'] - assign['A', 'Bristol'] - assign['D', 'Brighton'] >= -1;
   con pd1_A_Bristol_D_London : product['A', 'Bristol', 'D', 'London'] - assign['A', 'Bristol'] - assign['D', 'London'] >= -1;
   con pd1_A_Bristol_E_Bristol : product['A', 'Bristol', 'E', 'Bristol'] - assign['A', 'Bristol'] - assign['E', 'Bristol'] >= -1;
   con pd1_A_Bristol_E_Brighton : product['A', 'Bristol', 'E', 'Brighton'] - assign['A', 'Bristol'] - assign['E', 'Brighton'] >= -1;
   con pd1_A_Bristol_E_London : product['A', 'Bristol', 'E', 'London'] - assign['A', 'Bristol'] - assign['E', 'London'] >= -1;
   con pd1_A_Brighton_B_Bristol : product['A', 'Brighton', 'B', 'Bristol'] - assign['A', 'Brighton'] - assign['B', 'Bristol'] >= -1;
   con pd1_A_Brighton_B_Brighton : product['A', 'Brighton', 'B', 'Brighton'] - assign['A', 'Brighton'] - assign['B', 'Brighton'] >= -1;
   con pd1_A_Brighton_B_London : product['A', 'Brighton', 'B', 'London'] - assign['A', 'Brighton'] - assign['B', 'London'] >= -1;
   con pd1_A_Brighton_C_Bristol : product['A', 'Brighton', 'C', 'Bristol'] - assign['A', 'Brighton'] - assign['C', 'Bristol'] >= -1;
   con pd1_A_Brighton_C_Brighton : product['A', 'Brighton', 'C', 'Brighton'] - assign['A', 'Brighton'] - assign['C', 'Brighton'] >= -1;
   con pd1_A_Brighton_C_London : product['A', 'Brighton', 'C', 'London'] - assign['A', 'Brighton'] - assign['C', 'London'] >= -1;
   con pd1_A_Brighton_D_Bristol : product['A', 'Brighton', 'D', 'Bristol'] - assign['A', 'Brighton'] - assign['D', 'Bristol'] >= -1;
   con pd1_A_Brighton_D_Brighton : product['A', 'Brighton', 'D', 'Brighton'] - assign['A', 'Brighton'] - assign['D', 'Brighton'] >= -1;
   con pd1_A_Brighton_D_London : product['A', 'Brighton', 'D', 'London'] - assign['A', 'Brighton'] - assign['D', 'London'] >= -1;
   con pd1_A_Brighton_E_Bristol : product['A', 'Brighton', 'E', 'Bristol'] - assign['A', 'Brighton'] - assign['E', 'Bristol'] >= -1;
   con pd1_A_Brighton_E_Brighton : product['A', 'Brighton', 'E', 'Brighton'] - assign['A', 'Brighton'] - assign['E', 'Brighton'] >= -1;
   con pd1_A_Brighton_E_London : product['A', 'Brighton', 'E', 'London'] - assign['A', 'Brighton'] - assign['E', 'London'] >= -1;
   con pd1_A_London_B_Bristol : product['A', 'London', 'B', 'Bristol'] - assign['A', 'London'] - assign['B', 'Bristol'] >= -1;
   con pd1_A_London_B_Brighton : product['A', 'London', 'B', 'Brighton'] - assign['A', 'London'] - assign['B', 'Brighton'] >= -1;
   con pd1_A_London_B_London : product['A', 'London', 'B', 'London'] - assign['A', 'London'] - assign['B', 'London'] >= -1;
   con pd1_A_London_C_Bristol : product['A', 'London', 'C', 'Bristol'] - assign['A', 'London'] - assign['C', 'Bristol'] >= -1;
   con pd1_A_London_C_Brighton : product['A', 'London', 'C', 'Brighton'] - assign['A', 'London'] - assign['C', 'Brighton'] >= -1;
   con pd1_A_London_C_London : product['A', 'London', 'C', 'London'] - assign['A', 'London'] - assign['C', 'London'] >= -1;
   con pd1_A_London_D_Bristol : product['A', 'London', 'D', 'Bristol'] - assign['A', 'London'] - assign['D', 'Bristol'] >= -1;
   con pd1_A_London_D_Brighton : product['A', 'London', 'D', 'Brighton'] - assign['A', 'London'] - assign['D', 'Brighton'] >= -1;
   con pd1_A_London_D_London : product['A', 'London', 'D', 'London'] - assign['A', 'London'] - assign['D', 'London'] >= -1;
   con pd1_A_London_E_Bristol : product['A', 'London', 'E', 'Bristol'] - assign['A', 'London'] - assign['E', 'Bristol'] >= -1;
   con pd1_A_London_E_Brighton : product['A', 'London', 'E', 'Brighton'] - assign['A', 'London'] - assign['E', 'Brighton'] >= -1;
   con pd1_A_London_E_London : product['A', 'London', 'E', 'London'] - assign['A', 'London'] - assign['E', 'London'] >= -1;
   con pd1_B_Bristol_C_Bristol : product['B', 'Bristol', 'C', 'Bristol'] - assign['B', 'Bristol'] - assign['C', 'Bristol'] >= -1;
   con pd1_B_Bristol_C_Brighton : product['B', 'Bristol', 'C', 'Brighton'] - assign['B', 'Bristol'] - assign['C', 'Brighton'] >= -1;
   con pd1_B_Bristol_C_London : product['B', 'Bristol', 'C', 'London'] - assign['B', 'Bristol'] - assign['C', 'London'] >= -1;
   con pd1_B_Bristol_D_Bristol : product['B', 'Bristol', 'D', 'Bristol'] - assign['B', 'Bristol'] - assign['D', 'Bristol'] >= -1;
   con pd1_B_Bristol_D_Brighton : product['B', 'Bristol', 'D', 'Brighton'] - assign['B', 'Bristol'] - assign['D', 'Brighton'] >= -1;
   con pd1_B_Bristol_D_London : product['B', 'Bristol', 'D', 'London'] - assign['B', 'Bristol'] - assign['D', 'London'] >= -1;
   con pd1_B_Bristol_E_Bristol : product['B', 'Bristol', 'E', 'Bristol'] - assign['B', 'Bristol'] - assign['E', 'Bristol'] >= -1;
   con pd1_B_Bristol_E_Brighton : product['B', 'Bristol', 'E', 'Brighton'] - assign['B', 'Bristol'] - assign['E', 'Brighton'] >= -1;
   con pd1_B_Bristol_E_London : product['B', 'Bristol', 'E', 'London'] - assign['B', 'Bristol'] - assign['E', 'London'] >= -1;
   con pd1_B_Brighton_C_Bristol : product['B', 'Brighton', 'C', 'Bristol'] - assign['B', 'Brighton'] - assign['C', 'Bristol'] >= -1;
   con pd1_B_Brighton_C_Brighton : product['B', 'Brighton', 'C', 'Brighton'] - assign['B', 'Brighton'] - assign['C', 'Brighton'] >= -1;
   con pd1_B_Brighton_C_London : product['B', 'Brighton', 'C', 'London'] - assign['B', 'Brighton'] - assign['C', 'London'] >= -1;
   con pd1_B_Brighton_D_Bristol : product['B', 'Brighton', 'D', 'Bristol'] - assign['B', 'Brighton'] - assign['D', 'Bristol'] >= -1;
   con pd1_B_Brighton_D_Brighton : product['B', 'Brighton', 'D', 'Brighton'] - assign['B', 'Brighton'] - assign['D', 'Brighton'] >= -1;
   con pd1_B_Brighton_D_London : product['B', 'Brighton', 'D', 'London'] - assign['B', 'Brighton'] - assign['D', 'London'] >= -1;
   con pd1_B_Brighton_E_Bristol : product['B', 'Brighton', 'E', 'Bristol'] - assign['B', 'Brighton'] - assign['E', 'Bristol'] >= -1;
   con pd1_B_Brighton_E_Brighton : product['B', 'Brighton', 'E', 'Brighton'] - assign['B', 'Brighton'] - assign['E', 'Brighton'] >= -1;
   con pd1_B_Brighton_E_London : product['B', 'Brighton', 'E', 'London'] - assign['B', 'Brighton'] - assign['E', 'London'] >= -1;
   con pd1_B_London_C_Bristol : product['B', 'London', 'C', 'Bristol'] - assign['B', 'London'] - assign['C', 'Bristol'] >= -1;
   con pd1_B_London_C_Brighton : product['B', 'London', 'C', 'Brighton'] - assign['B', 'London'] - assign['C', 'Brighton'] >= -1;
   con pd1_B_London_C_London : product['B', 'London', 'C', 'London'] - assign['B', 'London'] - assign['C', 'London'] >= -1;
   con pd1_B_London_D_Bristol : product['B', 'London', 'D', 'Bristol'] - assign['B', 'London'] - assign['D', 'Bristol'] >= -1;
   con pd1_B_London_D_Brighton : product['B', 'London', 'D', 'Brighton'] - assign['B', 'London'] - assign['D', 'Brighton'] >= -1;
   con pd1_B_London_D_London : product['B', 'London', 'D', 'London'] - assign['B', 'London'] - assign['D', 'London'] >= -1;
   con pd1_B_London_E_Bristol : product['B', 'London', 'E', 'Bristol'] - assign['B', 'London'] - assign['E', 'Bristol'] >= -1;
   con pd1_B_London_E_Brighton : product['B', 'London', 'E', 'Brighton'] - assign['B', 'London'] - assign['E', 'Brighton'] >= -1;
   con pd1_B_London_E_London : product['B', 'London', 'E', 'London'] - assign['B', 'London'] - assign['E', 'London'] >= -1;
   con pd1_C_Bristol_D_Bristol : product['C', 'Bristol', 'D', 'Bristol'] - assign['C', 'Bristol'] - assign['D', 'Bristol'] >= -1;
   con pd1_C_Bristol_D_Brighton : product['C', 'Bristol', 'D', 'Brighton'] - assign['C', 'Bristol'] - assign['D', 'Brighton'] >= -1;
   con pd1_C_Bristol_D_London : product['C', 'Bristol', 'D', 'London'] - assign['C', 'Bristol'] - assign['D', 'London'] >= -1;
   con pd1_C_Bristol_E_Bristol : product['C', 'Bristol', 'E', 'Bristol'] - assign['C', 'Bristol'] - assign['E', 'Bristol'] >= -1;
   con pd1_C_Bristol_E_Brighton : product['C', 'Bristol', 'E', 'Brighton'] - assign['C', 'Bristol'] - assign['E', 'Brighton'] >= -1;
   con pd1_C_Bristol_E_London : product['C', 'Bristol', 'E', 'London'] - assign['C', 'Bristol'] - assign['E', 'London'] >= -1;
   con pd1_C_Brighton_D_Bristol : product['C', 'Brighton', 'D', 'Bristol'] - assign['C', 'Brighton'] - assign['D', 'Bristol'] >= -1;
   con pd1_C_Brighton_D_Brighton : product['C', 'Brighton', 'D', 'Brighton'] - assign['C', 'Brighton'] - assign['D', 'Brighton'] >= -1;
   con pd1_C_Brighton_D_London : product['C', 'Brighton', 'D', 'London'] - assign['C', 'Brighton'] - assign['D', 'London'] >= -1;
   con pd1_C_Brighton_E_Bristol : product['C', 'Brighton', 'E', 'Bristol'] - assign['C', 'Brighton'] - assign['E', 'Bristol'] >= -1;
   con pd1_C_Brighton_E_Brighton : product['C', 'Brighton', 'E', 'Brighton'] - assign['C', 'Brighton'] - assign['E', 'Brighton'] >= -1;
   con pd1_C_Brighton_E_London : product['C', 'Brighton', 'E', 'London'] - assign['C', 'Brighton'] - assign['E', 'London'] >= -1;
   con pd1_C_London_D_Bristol : product['C', 'London', 'D', 'Bristol'] - assign['C', 'London'] - assign['D', 'Bristol'] >= -1;
   con pd1_C_London_D_Brighton : product['C', 'London', 'D', 'Brighton'] - assign['C', 'London'] - assign['D', 'Brighton'] >= -1;
   con pd1_C_London_D_London : product['C', 'London', 'D', 'London'] - assign['C', 'London'] - assign['D', 'London'] >= -1;
   con pd1_C_London_E_Bristol : product['C', 'London', 'E', 'Bristol'] - assign['C', 'London'] - assign['E', 'Bristol'] >= -1;
   con pd1_C_London_E_Brighton : product['C', 'London', 'E', 'Brighton'] - assign['C', 'London'] - assign['E', 'Brighton'] >= -1;
   con pd1_C_London_E_London : product['C', 'London', 'E', 'London'] - assign['C', 'London'] - assign['E', 'London'] >= -1;
   con pd1_D_Bristol_E_Bristol : product['D', 'Bristol', 'E', 'Bristol'] - assign['D', 'Bristol'] - assign['E', 'Bristol'] >= -1;
   con pd1_D_Bristol_E_Brighton : product['D', 'Bristol', 'E', 'Brighton'] - assign['D', 'Bristol'] - assign['E', 'Brighton'] >= -1;
   con pd1_D_Bristol_E_London : product['D', 'Bristol', 'E', 'London'] - assign['D', 'Bristol'] - assign['E', 'London'] >= -1;
   con pd1_D_Brighton_E_Bristol : product['D', 'Brighton', 'E', 'Bristol'] - assign['D', 'Brighton'] - assign['E', 'Bristol'] >= -1;
   con pd1_D_Brighton_E_Brighton : product['D', 'Brighton', 'E', 'Brighton'] - assign['D', 'Brighton'] - assign['E', 'Brighton'] >= -1;
   con pd1_D_Brighton_E_London : product['D', 'Brighton', 'E', 'London'] - assign['D', 'Brighton'] - assign['E', 'London'] >= -1;
   con pd1_D_London_E_Bristol : product['D', 'London', 'E', 'Bristol'] - assign['D', 'London'] - assign['E', 'Bristol'] >= -1;
   con pd1_D_London_E_Brighton : product['D', 'London', 'E', 'Brighton'] - assign['D', 'London'] - assign['E', 'Brighton'] >= -1;
   con pd1_D_London_E_London : product['D', 'London', 'E', 'London'] - assign['D', 'London'] - assign['E', 'London'] >= -1;
   con pd2_A_Bristol_B_Bristol : product['A', 'Bristol', 'B', 'Bristol'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_B_Brighton : product['A', 'Bristol', 'B', 'Brighton'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_B_London : product['A', 'Bristol', 'B', 'London'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_C_Bristol : product['A', 'Bristol', 'C', 'Bristol'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_C_Brighton : product['A', 'Bristol', 'C', 'Brighton'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_C_London : product['A', 'Bristol', 'C', 'London'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_D_Bristol : product['A', 'Bristol', 'D', 'Bristol'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_D_Brighton : product['A', 'Bristol', 'D', 'Brighton'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_D_London : product['A', 'Bristol', 'D', 'London'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_E_Bristol : product['A', 'Bristol', 'E', 'Bristol'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_E_Brighton : product['A', 'Bristol', 'E', 'Brighton'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Bristol_E_London : product['A', 'Bristol', 'E', 'London'] - assign['A', 'Bristol'] <= 0;
   con pd2_A_Brighton_B_Bristol : product['A', 'Brighton', 'B', 'Bristol'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_B_Brighton : product['A', 'Brighton', 'B', 'Brighton'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_B_London : product['A', 'Brighton', 'B', 'London'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_C_Bristol : product['A', 'Brighton', 'C', 'Bristol'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_C_Brighton : product['A', 'Brighton', 'C', 'Brighton'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_C_London : product['A', 'Brighton', 'C', 'London'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_D_Bristol : product['A', 'Brighton', 'D', 'Bristol'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_D_Brighton : product['A', 'Brighton', 'D', 'Brighton'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_D_London : product['A', 'Brighton', 'D', 'London'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_E_Bristol : product['A', 'Brighton', 'E', 'Bristol'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_E_Brighton : product['A', 'Brighton', 'E', 'Brighton'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_Brighton_E_London : product['A', 'Brighton', 'E', 'London'] - assign['A', 'Brighton'] <= 0;
   con pd2_A_London_B_Bristol : product['A', 'London', 'B', 'Bristol'] - assign['A', 'London'] <= 0;
   con pd2_A_London_B_Brighton : product['A', 'London', 'B', 'Brighton'] - assign['A', 'London'] <= 0;
   con pd2_A_London_B_London : product['A', 'London', 'B', 'London'] - assign['A', 'London'] <= 0;
   con pd2_A_London_C_Bristol : product['A', 'London', 'C', 'Bristol'] - assign['A', 'London'] <= 0;
   con pd2_A_London_C_Brighton : product['A', 'London', 'C', 'Brighton'] - assign['A', 'London'] <= 0;
   con pd2_A_London_C_London : product['A', 'London', 'C', 'London'] - assign['A', 'London'] <= 0;
   con pd2_A_London_D_Bristol : product['A', 'London', 'D', 'Bristol'] - assign['A', 'London'] <= 0;
   con pd2_A_London_D_Brighton : product['A', 'London', 'D', 'Brighton'] - assign['A', 'London'] <= 0;
   con pd2_A_London_D_London : product['A', 'London', 'D', 'London'] - assign['A', 'London'] <= 0;
   con pd2_A_London_E_Bristol : product['A', 'London', 'E', 'Bristol'] - assign['A', 'London'] <= 0;
   con pd2_A_London_E_Brighton : product['A', 'London', 'E', 'Brighton'] - assign['A', 'London'] <= 0;
   con pd2_A_London_E_London : product['A', 'London', 'E', 'London'] - assign['A', 'London'] <= 0;
   con pd2_B_Bristol_C_Bristol : product['B', 'Bristol', 'C', 'Bristol'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Bristol_C_Brighton : product['B', 'Bristol', 'C', 'Brighton'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Bristol_C_London : product['B', 'Bristol', 'C', 'London'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Bristol_D_Bristol : product['B', 'Bristol', 'D', 'Bristol'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Bristol_D_Brighton : product['B', 'Bristol', 'D', 'Brighton'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Bristol_D_London : product['B', 'Bristol', 'D', 'London'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Bristol_E_Bristol : product['B', 'Bristol', 'E', 'Bristol'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Bristol_E_Brighton : product['B', 'Bristol', 'E', 'Brighton'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Bristol_E_London : product['B', 'Bristol', 'E', 'London'] - assign['B', 'Bristol'] <= 0;
   con pd2_B_Brighton_C_Bristol : product['B', 'Brighton', 'C', 'Bristol'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_Brighton_C_Brighton : product['B', 'Brighton', 'C', 'Brighton'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_Brighton_C_London : product['B', 'Brighton', 'C', 'London'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_Brighton_D_Bristol : product['B', 'Brighton', 'D', 'Bristol'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_Brighton_D_Brighton : product['B', 'Brighton', 'D', 'Brighton'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_Brighton_D_London : product['B', 'Brighton', 'D', 'London'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_Brighton_E_Bristol : product['B', 'Brighton', 'E', 'Bristol'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_Brighton_E_Brighton : product['B', 'Brighton', 'E', 'Brighton'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_Brighton_E_London : product['B', 'Brighton', 'E', 'London'] - assign['B', 'Brighton'] <= 0;
   con pd2_B_London_C_Bristol : product['B', 'London', 'C', 'Bristol'] - assign['B', 'London'] <= 0;
   con pd2_B_London_C_Brighton : product['B', 'London', 'C', 'Brighton'] - assign['B', 'London'] <= 0;
   con pd2_B_London_C_London : product['B', 'London', 'C', 'London'] - assign['B', 'London'] <= 0;
   con pd2_B_London_D_Bristol : product['B', 'London', 'D', 'Bristol'] - assign['B', 'London'] <= 0;
   con pd2_B_London_D_Brighton : product['B', 'London', 'D', 'Brighton'] - assign['B', 'London'] <= 0;
   con pd2_B_London_D_London : product['B', 'London', 'D', 'London'] - assign['B', 'London'] <= 0;
   con pd2_B_London_E_Bristol : product['B', 'London', 'E', 'Bristol'] - assign['B', 'London'] <= 0;
   con pd2_B_London_E_Brighton : product['B', 'London', 'E', 'Brighton'] - assign['B', 'London'] <= 0;
   con pd2_B_London_E_London : product['B', 'London', 'E', 'London'] - assign['B', 'London'] <= 0;
   con pd2_C_Bristol_D_Bristol : product['C', 'Bristol', 'D', 'Bristol'] - assign['C', 'Bristol'] <= 0;
   con pd2_C_Bristol_D_Brighton : product['C', 'Bristol', 'D', 'Brighton'] - assign['C', 'Bristol'] <= 0;
   con pd2_C_Bristol_D_London : product['C', 'Bristol', 'D', 'London'] - assign['C', 'Bristol'] <= 0;
   con pd2_C_Bristol_E_Bristol : product['C', 'Bristol', 'E', 'Bristol'] - assign['C', 'Bristol'] <= 0;
   con pd2_C_Bristol_E_Brighton : product['C', 'Bristol', 'E', 'Brighton'] - assign['C', 'Bristol'] <= 0;
   con pd2_C_Bristol_E_London : product['C', 'Bristol', 'E', 'London'] - assign['C', 'Bristol'] <= 0;
   con pd2_C_Brighton_D_Bristol : product['C', 'Brighton', 'D', 'Bristol'] - assign['C', 'Brighton'] <= 0;
   con pd2_C_Brighton_D_Brighton : product['C', 'Brighton', 'D', 'Brighton'] - assign['C', 'Brighton'] <= 0;
   con pd2_C_Brighton_D_London : product['C', 'Brighton', 'D', 'London'] - assign['C', 'Brighton'] <= 0;
   con pd2_C_Brighton_E_Bristol : product['C', 'Brighton', 'E', 'Bristol'] - assign['C', 'Brighton'] <= 0;
   con pd2_C_Brighton_E_Brighton : product['C', 'Brighton', 'E', 'Brighton'] - assign['C', 'Brighton'] <= 0;
   con pd2_C_Brighton_E_London : product['C', 'Brighton', 'E', 'London'] - assign['C', 'Brighton'] <= 0;
   con pd2_C_London_D_Bristol : product['C', 'London', 'D', 'Bristol'] - assign['C', 'London'] <= 0;
   con pd2_C_London_D_Brighton : product['C', 'London', 'D', 'Brighton'] - assign['C', 'London'] <= 0;
   con pd2_C_London_D_London : product['C', 'London', 'D', 'London'] - assign['C', 'London'] <= 0;
   con pd2_C_London_E_Bristol : product['C', 'London', 'E', 'Bristol'] - assign['C', 'London'] <= 0;
   con pd2_C_London_E_Brighton : product['C', 'London', 'E', 'Brighton'] - assign['C', 'London'] <= 0;
   con pd2_C_London_E_London : product['C', 'London', 'E', 'London'] - assign['C', 'London'] <= 0;
   con pd2_D_Bristol_E_Bristol : product['D', 'Bristol', 'E', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd2_D_Bristol_E_Brighton : product['D', 'Bristol', 'E', 'Brighton'] - assign['D', 'Bristol'] <= 0;
   con pd2_D_Bristol_E_London : product['D', 'Bristol', 'E', 'London'] - assign['D', 'Bristol'] <= 0;
   con pd2_D_Brighton_E_Bristol : product['D', 'Brighton', 'E', 'Bristol'] - assign['D', 'Brighton'] <= 0;
   con pd2_D_Brighton_E_Brighton : product['D', 'Brighton', 'E', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd2_D_Brighton_E_London : product['D', 'Brighton', 'E', 'London'] - assign['D', 'Brighton'] <= 0;
   con pd2_D_London_E_Bristol : product['D', 'London', 'E', 'Bristol'] - assign['D', 'London'] <= 0;
   con pd2_D_London_E_Brighton : product['D', 'London', 'E', 'Brighton'] - assign['D', 'London'] <= 0;
   con pd2_D_London_E_London : product['D', 'London', 'E', 'London'] - assign['D', 'London'] <= 0;
   con pd3_A_Bristol_B_Bristol : product['A', 'Bristol', 'B', 'Bristol'] - assign['B', 'Bristol'] <= 0;
   con pd3_A_Bristol_B_Brighton : product['A', 'Bristol', 'B', 'Brighton'] - assign['B', 'Brighton'] <= 0;
   con pd3_A_Bristol_B_London : product['A', 'Bristol', 'B', 'London'] - assign['B', 'London'] <= 0;
   con pd3_A_Bristol_C_Bristol : product['A', 'Bristol', 'C', 'Bristol'] - assign['C', 'Bristol'] <= 0;
   con pd3_A_Bristol_C_Brighton : product['A', 'Bristol', 'C', 'Brighton'] - assign['C', 'Brighton'] <= 0;
   con pd3_A_Bristol_C_London : product['A', 'Bristol', 'C', 'London'] - assign['C', 'London'] <= 0;
   con pd3_A_Bristol_D_Bristol : product['A', 'Bristol', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_A_Bristol_D_Brighton : product['A', 'Bristol', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_A_Bristol_D_London : product['A', 'Bristol', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_A_Bristol_E_Bristol : product['A', 'Bristol', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_A_Bristol_E_Brighton : product['A', 'Bristol', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_A_Bristol_E_London : product['A', 'Bristol', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_A_Brighton_B_Bristol : product['A', 'Brighton', 'B', 'Bristol'] - assign['B', 'Bristol'] <= 0;
   con pd3_A_Brighton_B_Brighton : product['A', 'Brighton', 'B', 'Brighton'] - assign['B', 'Brighton'] <= 0;
   con pd3_A_Brighton_B_London : product['A', 'Brighton', 'B', 'London'] - assign['B', 'London'] <= 0;
   con pd3_A_Brighton_C_Bristol : product['A', 'Brighton', 'C', 'Bristol'] - assign['C', 'Bristol'] <= 0;
   con pd3_A_Brighton_C_Brighton : product['A', 'Brighton', 'C', 'Brighton'] - assign['C', 'Brighton'] <= 0;
   con pd3_A_Brighton_C_London : product['A', 'Brighton', 'C', 'London'] - assign['C', 'London'] <= 0;
   con pd3_A_Brighton_D_Bristol : product['A', 'Brighton', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_A_Brighton_D_Brighton : product['A', 'Brighton', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_A_Brighton_D_London : product['A', 'Brighton', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_A_Brighton_E_Bristol : product['A', 'Brighton', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_A_Brighton_E_Brighton : product['A', 'Brighton', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_A_Brighton_E_London : product['A', 'Brighton', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_A_London_B_Bristol : product['A', 'London', 'B', 'Bristol'] - assign['B', 'Bristol'] <= 0;
   con pd3_A_London_B_Brighton : product['A', 'London', 'B', 'Brighton'] - assign['B', 'Brighton'] <= 0;
   con pd3_A_London_B_London : product['A', 'London', 'B', 'London'] - assign['B', 'London'] <= 0;
   con pd3_A_London_C_Bristol : product['A', 'London', 'C', 'Bristol'] - assign['C', 'Bristol'] <= 0;
   con pd3_A_London_C_Brighton : product['A', 'London', 'C', 'Brighton'] - assign['C', 'Brighton'] <= 0;
   con pd3_A_London_C_London : product['A', 'London', 'C', 'London'] - assign['C', 'London'] <= 0;
   con pd3_A_London_D_Bristol : product['A', 'London', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_A_London_D_Brighton : product['A', 'London', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_A_London_D_London : product['A', 'London', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_A_London_E_Bristol : product['A', 'London', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_A_London_E_Brighton : product['A', 'London', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_A_London_E_London : product['A', 'London', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_B_Bristol_C_Bristol : product['B', 'Bristol', 'C', 'Bristol'] - assign['C', 'Bristol'] <= 0;
   con pd3_B_Bristol_C_Brighton : product['B', 'Bristol', 'C', 'Brighton'] - assign['C', 'Brighton'] <= 0;
   con pd3_B_Bristol_C_London : product['B', 'Bristol', 'C', 'London'] - assign['C', 'London'] <= 0;
   con pd3_B_Bristol_D_Bristol : product['B', 'Bristol', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_B_Bristol_D_Brighton : product['B', 'Bristol', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_B_Bristol_D_London : product['B', 'Bristol', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_B_Bristol_E_Bristol : product['B', 'Bristol', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_B_Bristol_E_Brighton : product['B', 'Bristol', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_B_Bristol_E_London : product['B', 'Bristol', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_B_Brighton_C_Bristol : product['B', 'Brighton', 'C', 'Bristol'] - assign['C', 'Bristol'] <= 0;
   con pd3_B_Brighton_C_Brighton : product['B', 'Brighton', 'C', 'Brighton'] - assign['C', 'Brighton'] <= 0;
   con pd3_B_Brighton_C_London : product['B', 'Brighton', 'C', 'London'] - assign['C', 'London'] <= 0;
   con pd3_B_Brighton_D_Bristol : product['B', 'Brighton', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_B_Brighton_D_Brighton : product['B', 'Brighton', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_B_Brighton_D_London : product['B', 'Brighton', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_B_Brighton_E_Bristol : product['B', 'Brighton', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_B_Brighton_E_Brighton : product['B', 'Brighton', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_B_Brighton_E_London : product['B', 'Brighton', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_B_London_C_Bristol : product['B', 'London', 'C', 'Bristol'] - assign['C', 'Bristol'] <= 0;
   con pd3_B_London_C_Brighton : product['B', 'London', 'C', 'Brighton'] - assign['C', 'Brighton'] <= 0;
   con pd3_B_London_C_London : product['B', 'London', 'C', 'London'] - assign['C', 'London'] <= 0;
   con pd3_B_London_D_Bristol : product['B', 'London', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_B_London_D_Brighton : product['B', 'London', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_B_London_D_London : product['B', 'London', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_B_London_E_Bristol : product['B', 'London', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_B_London_E_Brighton : product['B', 'London', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_B_London_E_London : product['B', 'London', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_C_Bristol_D_Bristol : product['C', 'Bristol', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_C_Bristol_D_Brighton : product['C', 'Bristol', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_C_Bristol_D_London : product['C', 'Bristol', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_C_Bristol_E_Bristol : product['C', 'Bristol', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_C_Bristol_E_Brighton : product['C', 'Bristol', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_C_Bristol_E_London : product['C', 'Bristol', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_C_Brighton_D_Bristol : product['C', 'Brighton', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_C_Brighton_D_Brighton : product['C', 'Brighton', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_C_Brighton_D_London : product['C', 'Brighton', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_C_Brighton_E_Bristol : product['C', 'Brighton', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_C_Brighton_E_Brighton : product['C', 'Brighton', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_C_Brighton_E_London : product['C', 'Brighton', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_C_London_D_Bristol : product['C', 'London', 'D', 'Bristol'] - assign['D', 'Bristol'] <= 0;
   con pd3_C_London_D_Brighton : product['C', 'London', 'D', 'Brighton'] - assign['D', 'Brighton'] <= 0;
   con pd3_C_London_D_London : product['C', 'London', 'D', 'London'] - assign['D', 'London'] <= 0;
   con pd3_C_London_E_Bristol : product['C', 'London', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_C_London_E_Brighton : product['C', 'London', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_C_London_E_London : product['C', 'London', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_D_Bristol_E_Bristol : product['D', 'Bristol', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_D_Bristol_E_Brighton : product['D', 'Bristol', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_D_Bristol_E_London : product['D', 'Bristol', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_D_Brighton_E_Bristol : product['D', 'Brighton', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_D_Brighton_E_Brighton : product['D', 'Brighton', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_D_Brighton_E_London : product['D', 'Brighton', 'E', 'London'] - assign['E', 'London'] <= 0;
   con pd3_D_London_E_Bristol : product['D', 'London', 'E', 'Bristol'] - assign['E', 'Bristol'] <= 0;
   con pd3_D_London_E_Brighton : product['D', 'London', 'E', 'Brighton'] - assign['E', 'Brighton'] <= 0;
   con pd3_D_London_E_London : product['D', 'London', 'E', 'London'] - assign['E', 'London'] <= 0;
   solve;
quit;