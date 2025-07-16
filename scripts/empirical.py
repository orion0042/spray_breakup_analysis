def compare_with_correlations(Lb, SMD, rho, mu, sigma, pressure, fluid):
    # Compute dimensionless numbers
    from math import sqrt
    U = sqrt(2 * pressure * 1e5 / rho)   # velocity estimate [m/s]
    D = 0.001                            # example or ask user (1 mm); adapt if needed
    We = rho * U**2 * D / sigma
    Re = rho * U * D / mu
    Oh = mu / sqrt(rho * sigma * D)
    print(f"\n-- Dimensionless numbers --")
    print(f"  Weber: {We:.2f}\n  Reynolds: {Re:.2f}\n  Ohnesorge: {Oh:.3f}")
    # Lefebvre SMD: SMD = K*(sigma/(rho_g*U^2))^0.5
    K = 0.5
    SMD_lev = K * (sigma/(rho*U**2))**0.5 * 1e3  # mm
    print(f"Lefebvre SMD prediction: {SMD_lev:.3f} mm")
    print(f"  Experiment SMD: {SMD:.3f} mm")
    print(f"  Rel Error: {(SMD_lev-SMD)*100/SMD:.1f} %")
    # Breakup length example model
    a, b = 15, 0.2
    Lb_pred = a * D * We**b * 1e3  # in mm
    print(f"Model breakup length: {Lb_pred:.2f} mm vs Experiment: {Lb:.2f} mm")
    print(f"  Rel Error: {(Lb_pred-Lb)*100/Lb:.1f} %")
