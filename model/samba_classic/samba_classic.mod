// SAMBA classic MVP Dynare shell.
// WBS-057: sourced from docs/wbs057_equation_sourcing.md.
// Do not add future-stage commands, include files, data, or outputs here.

var
  r_t z_r q risk nfa nx external_loans
  sp_target sp g b tax_rate
  pi_a v_a z_a
  c_o c c_rt q_k i k wn labor
  v_m v_g v_i v_f v_x
  pi_m pi_g pi_i pi_f pi_x
  y q_y pi_y
;

// WP239 Appendix C.39 and C.7 write NFA and capital as t+1 stock laws.
predetermined_variables nfa k;

varexo
  pi pi_target y_gap r_star pi_star
  risk_dom z_q z_z z_c z_i z_w z_p z_px z_g
  eps_monetary eps_risk eps_sp_target eps_tax eps_admin
  q_f q_g q_i q_m q_m_star q_x_star q_d y_d r_k mc mc_x
  m_c m_i m_x m x
;

parameters
  rho_r phi_pi phi_y r_ss psi_nfa nfa_ss rho_risk
  rho_sp_target phi_b alpha_a_fx alpha_a_mc rho_admin
  theta_admin chi_admin
  share_c_y share_g_y share_i_y share_x_y share_m_y tax_share_T
  share_rule_thumb_c beta_tilde eta_labor_inverse_elasticity
  gross_bgp_growth habit_persistence intertemporal_eos_inverse
  capital_depreciation production_labor_share investment_adjustment_cost
  external_financing_share_c external_financing_share_i external_financing_share_x
  external_debt_lom_adjustment domestic_debt_lom_adjustment b_ss
  pi_target_gross_ss foreign_inflation_gross_ss foreign_rate_gross_ss
  country_risk_gross_ss fiscal_surplus_reaction fiscal_surplus_target_coeff
  tax_rate_persistence free_price_indexation government_price_indexation
  investment_price_indexation import_price_indexation export_price_indexation
  rho_z_c rho_z_z rho_z_i lambda_w lambda_m lambda_g lambda_i lambda_f lambda_x
;

@#include "calibration.m"

// WBS-057 formula/weight mappings from docs/03_calibration_notes.md.
share_c_y = 0.62;
share_g_y = 0.20;
share_i_y = 0.17;
share_x_y = 0.13;
share_m_y = 0.12;
tax_share_T = 0.35;
share_rule_thumb_c = 0.40;
beta_tilde = 0.989;
eta_labor_inverse_elasticity = 1.00;
gross_bgp_growth = 1.009;
habit_persistence = 0.74;
intertemporal_eos_inverse = 1.30;
capital_depreciation = 0.015;
production_labor_share = 0.8;
investment_adjustment_cost = 3.42;
external_financing_share_c = 0.5;
external_financing_share_i = 0.5;
external_financing_share_x = 0.5;
external_debt_lom_adjustment = 0.0397;
domestic_debt_lom_adjustment = 0.53;
b_ss = 2.00;
pi_target_gross_ss = 1.011;
foreign_inflation_gross_ss = 1.0064;
foreign_rate_gross_ss = 1.0074;
country_risk_gross_ss = 1.014;
fiscal_surplus_reaction = 0.49;
fiscal_surplus_target_coeff = 0.41;
tax_rate_persistence = 0.80;
free_price_indexation = 0.33;
government_price_indexation = 0.49;
investment_price_indexation = 0.55;
import_price_indexation = 0.65;
export_price_indexation = 0.35;

model(linear);
  # pi_4_lead = 0.25*(pi(+1) + pi(+2) + pi(+3) + pi(+4));
  # pi_target_4_lead = 0.25*(pi_target(+1) + pi_target(+2) + pi_target(+3) + pi_target(+4));
  # pi_target_lagavg = 0.25*(pi_target(-3) + pi_target(-2) + pi_target(-1) + pi_target);
  # lambda_bstar = foreign_rate_gross_ss*country_risk_gross_ss/(foreign_inflation_gross_ss*gross_bgp_growth);
  # rk_discount = beta_tilde*((1-capital_depreciation)/gross_bgp_growth);
  # capital_weight = (1-capital_depreciation)/gross_bgp_growth;
  # mrs = eta_labor_inverse_elasticity*labor + intertemporal_eos_inverse/(1-habit_persistence)*(c_o - habit_persistence*(c_o(-1)-z_z));

  [name='EQ-MON-001 C.28']
  r_t = rho_r*r_t(-1) + (1-rho_r)*(pi_target_lagavg + phi_pi*(pi_4_lead - pi_target_4_lead) + phi_y*y_gap) + z_r;

  [name='EQ-MON-003 C.60']
  z_r = eps_monetary;

  [name='EQ-EXT-001 C.4']
  q = q(+1) - (r_t + risk_dom - pi(+1)) + (r_star + risk - pi_star(+1)) + z_q;

  [name='EQ-EXT-002 C.50']
  risk = rho_risk*risk(-1) + eps_risk;

  [name='EQ-EXT-003 C.37']
  external_loans =
    external_financing_share_c*share_m_y*(foreign_rate_gross_ss*country_risk_gross_ss*(r_star+risk) + (foreign_rate_gross_ss*country_risk_gross_ss-1)*(q_m+m_c-q_y-y))
    + external_financing_share_i*share_m_y*(foreign_rate_gross_ss*country_risk_gross_ss*(r_star+risk) + (foreign_rate_gross_ss*country_risk_gross_ss-1)*(q_m+m_i-q_y-y))
    + external_financing_share_x*share_m_y*(foreign_rate_gross_ss*country_risk_gross_ss*(r_star+risk) + (foreign_rate_gross_ss*country_risk_gross_ss-1)*(q_m+m_x-q_y-y));

  [name='EQ-EXT-003 C.38']
  nx = share_x_y*(q+q_x_star+x) - share_m_y*(q+q_m_star+m) - (share_x_y-share_m_y)*(q_y+y);

  [name='EQ-EXT-003 C.39']
  nfa(+1) = lambda_bstar*nfa + foreign_rate_gross_ss*country_risk_gross_ss*(nx-external_loans) + nfa_ss*(r_star+risk)
    + lambda_bstar*nfa_ss*(y(-1)-y-pi_y-z_z+q-q(-1)+pi-pi_star);

  [name='EQ-FISC-001 C.31']
  sp_target = rho_sp_target*sp_target(-1) + phi_b*b + eps_sp_target;

  [name='EQ-FISC-002 C.30']
  sp = fiscal_surplus_reaction*sp(-1) + fiscal_surplus_target_coeff*sp_target - share_g_y*z_g;

  [name='EQ-FISC-002 C.33']
  g = (1/share_g_y)*(tax_rate - sp) + y + q_y - q_g;

  [name='EQ-FISC-003 C.34']
  b = domestic_debt_lom_adjustment*b(-1) + b_ss*r_t - r_ss*sp + domestic_debt_lom_adjustment*b_ss*(y(-1)-y-pi_y-z_z);

  [name='EQ-FISC-004 C.32']
  tax_rate = tax_rate_persistence*tax_rate(-1) + eps_tax;

  [name='EQ-PRICE-001 C.22']
  pi_a = theta_admin*v_a + (1-theta_admin)*pi_target;

  [name='EQ-PRICE-001 C.23']
  v_a = chi_admin*(pi(-1)+pi(-2)+pi(-3)+pi(-4) + alpha_a_fx*(q(-1)-q(-5)) + alpha_a_mc*(mc(-1)-mc(-5)))
    + (1-chi_admin)*q_f + (1/theta_admin)*z_a;

  [name='EQ-PRICE-002 C.58']
  z_a = rho_admin*z_a(-1) + eps_admin;

  [name='EQ-HH-001 C.1']
  c_o = -habit_persistence/(1+habit_persistence)*c_o(-1) + 1/(1+habit_persistence)*c_o(+1)
    - (1-habit_persistence)/(intertemporal_eos_inverse*(1+habit_persistence))*(r_t+risk_dom-pi(+1))
    + (rho_z_z-habit_persistence)/(1+habit_persistence)*z_z
    - ((1-rho_z_c)*(1-habit_persistence))/(intertemporal_eos_inverse*(1+habit_persistence))*z_c;

  [name='EQ-HH-002 C.3']
  c = share_rule_thumb_c*c_rt + (1-share_rule_thumb_c)*c_o;

  [name='EQ-HH-004 C.2']
  c_rt = wn + labor - tax_share_T/(1-tax_share_T)*tax_rate;

  [name='EQ-HH-001 C.5']
  q_k = rk_discount*q_k(+1) + (1-rk_discount)*r_k(+1) - (r_t+risk_dom-pi(+1));

  [name='EQ-FIRM-003 C.6']
  i = 1/(1+beta_tilde)*i(-1) + beta_tilde/(1+beta_tilde)*i(+1)
    + (q_k-q_i)/(investment_adjustment_cost*gross_bgp_growth^2*(1+beta_tilde))
    - (1-rho_z_i*beta_tilde)/(1+beta_tilde)*z_z
    + (1-rho_z_i)*beta_tilde/(1+beta_tilde)*z_i;

  [name='EQ-FIRM-003 C.7']
  k(+1) = capital_weight*(k-z_z) + (1-capital_weight)*i;

  [name='EQ-HH-003 C.10']
  wn-wn(-1) = free_price_indexation/(1+beta_tilde*free_price_indexation)*(wn(-1)-wn(-2))
    + beta_tilde/(1+beta_tilde*free_price_indexation)*(wn(+1)-wn)
    + lambda_w*(mrs-wn) + z_w
    + 1/(1+beta_tilde*free_price_indexation)*(pi(-1)+z_z(-1))
    - (1+beta_tilde)/(1+beta_tilde*free_price_indexation)*(pi+z_z)
    + beta_tilde/(1+beta_tilde*free_price_indexation)*(pi(+1)+z_z(+1));

  [name='EQ-HH-003 C.13']
  labor = production_labor_share*(q_d+y_d-wn);

  [name='EQ-FIRM-002 C.14 indexation']
  v_m = import_price_indexation*pi_m(-1);

  [name='EQ-FIRM-002 C.19 indexation H=G']
  v_g = government_price_indexation*pi_g(-1);

  [name='EQ-FIRM-002 C.19 indexation H=I']
  v_i = investment_price_indexation*pi_i(-1);

  [name='EQ-FIRM-002 C.21 indexation']
  v_f = free_price_indexation*pi_f(-1);

  [name='EQ-FIRM-002 C.26 indexation']
  v_x = export_price_indexation*pi_x(-1);

  [name='EQ-FIRM-002 C.14']
  pi_m - v_m = lambda_m*(q+q_m_star-q_m) + beta_tilde*(pi_m(+1)-v_m(+1));

  [name='EQ-FIRM-002 C.18 H=G']
  pi_g - v_g = lambda_g*(mc-q_g) + beta_tilde*(pi_g(+1)-v_g(+1)) + z_p;

  [name='EQ-FIRM-002 C.18 H=I']
  pi_i - v_i = lambda_i*(mc-q_i) + beta_tilde*(pi_i(+1)-v_i(+1)) + z_p;

  [name='EQ-FIRM-002 C.20']
  pi_f - v_f = lambda_f*(mc-q_f) + beta_tilde*(pi_f(+1)-v_f(+1)) + z_p;

  [name='EQ-FIRM-002 C.25']
  pi_x - v_x = lambda_x*(mc_x-q_x_star-q) + beta_tilde*(pi_x(+1)-v_x(+1)) + z_px;

  [name='EQ-AGG-003 C.40']
  y = share_c_y*c + share_i_y*i + share_g_y*g + share_x_y*x - share_m_y*m;

  [name='EQ-AGG-003 C.41']
  q_y = share_g_y*q_g + share_i_y*q_i + share_x_y*(q+q_x_star) - share_m_y*(q+q_m_star);

  [name='EQ-AGG-003 C.42']
  pi_y = pi + q_y - q_y(-1);
end;

@#include "shocks.inc"
@#include "observables.inc"

initval;
  r_t = 0;
  z_r = 0;
  q = 0;
  risk = 0;
  nfa = 0;
  nx = 0;
  external_loans = 0;
  sp_target = 0;
  sp = 0;
  g = 0;
  b = 0;
  tax_rate = 0;
  pi_a = 0;
  v_a = 0;
  z_a = 0;
  c_o = 0;
  c = 0;
  c_rt = 0;
  q_k = 0;
  i = 0;
  k = 0;
  wn = 0;
  labor = 0;
  v_m = 0;
  v_g = 0;
  v_i = 0;
  v_f = 0;
  v_x = 0;
  pi_m = 0;
  pi_g = 0;
  pi_i = 0;
  pi_f = 0;
  pi_x = 0;
  y = 0;
  q_y = 0;
  pi_y = 0;
end;
