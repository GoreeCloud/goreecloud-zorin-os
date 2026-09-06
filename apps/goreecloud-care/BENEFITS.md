# Benefits

- **Predictable:** every deletion category is previewed before cleanup, and scanning never deletes anything.
- **Least privilege:** normal user maintenance stays unprivileged; only explicitly system-level actions authenticate through PolicyKit.
- **Truthful:** memory-cache reclaim is described as temporary cache reclaim, not a magical RAM or performance boost.
- **Private:** no telemetry, advertising, cloud upload, or remote service is required for core maintenance.
- **Recoverability-aware:** permanent Trash deletion is isolated behind explicit confirmation rather than bundled into routine cleanup.
- **Native:** integrates with the Linux desktop using GTK, ATK/AT-SPI, and PolicyKit instead of wrapping an unrelated cleaner product.
- **Accessible:** keyboard traversal, visible focus, HighContrast behavior, large-text adaptation, constrained-window layout, and assistive-technology semantics are treated as acceptance requirements rather than optional polish.
- **Transparent:** users can see category sizes, item counts, disk headroom, memory availability, and file-cache estimates before deciding what to do.
- **Actionable without being aggressive:** Care can surface useful maintenance opportunities without turning every finding into an automatic deletion recommendation.
- **Support-friendly:** dev13 can produce a human-readable local maintenance report for troubleshooting without performing maintenance.
- **Automation-ready:** dev13 can emit machine-readable JSON for local scripts and future governed GoreeCloud Manager/Metrics/Notify integrations.
- **Privacy-safe by default:** generated reports omit candidate file paths, filenames, and raw scan-error strings unless a future explicit diagnostic workflow is separately designed and approved.
- **Auditable:** fixed cleanup categories, allowlisted privileged actions, exact package versions, tests, Platform Contract evidence, and Development lifecycle labeling make behavior easier to review.
- **Conservative under failure:** errors remain visible, failed items are not counted as successful deletion, and cancellation is never presented as success.
- **Low lock-in:** the current application stores no proprietary durable user dataset and its dev13 report format is plain text or JSON.
- **Extensible:** the maintenance engine, reporting layer, GTK interface, and Platform Contract can grow into storage intelligence, system-health insights, diagnostics, and safe guided maintenance without weakening the existing deletion boundaries.
- **Human-centered:** recommendations are intended to explain what can be reclaimed, why it is considered safe, what requires privilege, and what cannot be undone before the user acts.
