// WBS-069 source-backed priors include.
// Generated from docs/04_estimation_strategy.md WBS-068 Source-Backed Priors Table.
// Sources: BCB WP239 Table 3, PDF pages 98-99 / printed pages 97-98.
// This file defines priors only. It does not start estimation or create outputs.

estimated_params;
  // PRIOR-001 gamma_R, WP239 Table 3 Taylor rule.
  rho_r, beta_pdf, 0.60, 0.15;
  // PRIOR-002 rho_Bstar, WP239 Table 3 autoregressive shocks.
  rho_risk, beta_pdf, 0.50, 0.25;
  // PRIOR-003 rho_Sbar, WP239 Table 3 autoregressive shocks.
  rho_sp_target, beta_pdf, 0.50, 0.25;
  // PRIOR-004 phi_B, WP239 Table 3 fiscal rule.
  phi_b, inv_gamma_pdf, 0.05, 0.15;
  // PRIOR-005 vartheta_A_1, WP239 Table 3 administered price rule.
  alpha_a_fx, beta_pdf, 0.05, 0.03;
  // PRIOR-006 vartheta_A_2, WP239 Table 3 administered price rule.
  alpha_a_mc, beta_pdf, 0.20, 0.05;
  // PRIOR-007 rho_A, WP239 Table 3 autoregressive shocks.
  rho_admin, beta_pdf, 0.50, 0.25;
  // PRIOR-008 rho_C, WP239 Table 3 autoregressive shocks.
  rho_z_c, beta_pdf, 0.50, 0.25;
  // PRIOR-009 rho_Z, WP239 Table 3 autoregressive shocks.
  rho_z_z, beta_pdf, 0.50, 0.25;
  // PRIOR-010 rho_I, WP239 Table 3 autoregressive shocks.
  rho_z_i, beta_pdf, 0.50, 0.25;
  // PRIOR-011 epsilon_B, WP239 Table 3 exogenous shocks.
  stderr risk_dom, inv_gamma_pdf, 1.0, inf;
  // PRIOR-012 epsilon_I, WP239 Table 3 exogenous shocks.
  stderr z_i, inv_gamma_pdf, 1.0, inf;
  // PRIOR-013 epsilon_C, WP239 Table 3 exogenous shocks.
  stderr z_c, inv_gamma_pdf, 1.0, inf;
  // PRIOR-014 epsilon_A, WP239 Table 3 exogenous shocks.
  stderr eps_admin, inv_gamma_pdf, 1.0, inf;
  // PRIOR-015 epsilon_P, WP239 Table 3 exogenous shocks.
  stderr z_p, inv_gamma_pdf, 1.0, inf;
  // PRIOR-016 epsilon_PiC, WP239 Table 3 exogenous shocks.
  stderr pi, inv_gamma_pdf, 1.0, inf;
  // PRIOR-017 epsilon_W, WP239 Table 3 exogenous shocks.
  stderr z_w, inv_gamma_pdf, 1.0, inf;
  // PRIOR-018 epsilon_Z, WP239 Table 3 exogenous shocks.
  stderr z_z, inv_gamma_pdf, 1.0, inf;
  // PRIOR-019 epsilon_Q, WP239 Table 3 exogenous shocks.
  stderr z_q, inv_gamma_pdf, 1.0, inf;
  // PRIOR-020 epsilon_Bstar, WP239 Table 3 exogenous shocks.
  stderr eps_risk, inv_gamma_pdf, 1.0, inf;
  // PRIOR-021 epsilon_G, WP239 Table 3 exogenous shocks.
  stderr z_g, inv_gamma_pdf, 1.0, inf;
  // PRIOR-022 epsilon_T, WP239 Table 3 exogenous shocks.
  stderr eps_tax, inv_gamma_pdf, 1.0, inf;
  // PRIOR-023 epsilon_Sbar, WP239 Table 3 exogenous shocks.
  stderr eps_sp_target, inv_gamma_pdf, 1.0, inf;
  // PRIOR-024 epsilon_R, WP239 Table 3 exogenous shocks.
  stderr eps_monetary, inv_gamma_pdf, 1.0, inf;
  // PRIOR-025 epsilon_Pstar, WP239 Table 3 exogenous shocks.
  stderr z_px, inv_gamma_pdf, 1.0, inf;
  // PRIOR-026 epsilon_Pistar, WP239 Table 3 exogenous shocks.
  stderr pi_star, inv_gamma_pdf, 1.0, inf;
  // PRIOR-027 epsilon_Rstar, WP239 Table 3 exogenous shocks.
  stderr r_star, inv_gamma_pdf, 1.0, inf;
  // PRIOR-028 epsilon_QMstar, WP239 Table 3 exogenous shocks.
  stderr q_m_star, inv_gamma_pdf, 1.0, inf;
end;
