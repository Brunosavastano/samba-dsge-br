// WBS-058 shock standard deviations.
// Source: WP239 Table 3, p. 98; posterior means used as Dynare stderr values.
// These are standard deviations, not squared variances.

shocks;
  // epsilon_B -> risk_dom
  var risk_dom;
  stderr 0.57;

  // epsilon_I -> z_i
  var z_i;
  stderr 3.54;

  // epsilon_C -> z_c
  var z_c;
  stderr 8.80;

  // epsilon_A -> eps_admin
  var eps_admin;
  stderr 1.40;

  // epsilon_P -> z_p
  var z_p;
  stderr 0.79;

  // epsilon_PiC -> pi
  var pi;
  stderr 0.14;

  // epsilon_W -> z_w
  var z_w;
  stderr 1.38;

  // epsilon_Z -> z_z
  var z_z;
  stderr 0.17;

  // epsilon_Q -> z_q
  var z_q;
  stderr 0.80;

  // epsilon_Bstar -> eps_risk
  var eps_risk;
  stderr 0.38;

  // epsilon_G -> z_g
  var z_g;
  stderr 1.73;

  // epsilon_T -> eps_tax
  var eps_tax;
  stderr 0.48;

  // epsilon_Sbar -> eps_sp_target
  var eps_sp_target;
  stderr 0.29;

  // epsilon_R -> eps_monetary
  var eps_monetary;
  stderr 0.32;

  // epsilon_Pstar -> z_px
  var z_px;
  stderr 3.89;

  // epsilon_Pistar -> pi_star
  var pi_star;
  stderr 0.85;

  // epsilon_Rstar -> r_star
  var r_star;
  stderr 0.19;

  // epsilon_QMstar -> q_m_star
  var q_m_star;
  stderr 1.85;
end;
