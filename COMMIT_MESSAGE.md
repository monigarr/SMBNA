docs: Reorganize documentation into public/private split per security best practices

Reorganize all documentation following conservative, reviewer-approved split
between public and private documentation. This aligns with best practices used
by research labs, defense contractors, and dual-use academic projects.

## Documentation Reorganization

### Public Documentation (docs/ - committed to GitHub)

Created sanitized public versions of documentation:

- **architecture_overview.md** - High-level architecture only
  - Conceptual diagrams and block-level architecture
  - Data flow (inputs → arbitration → outputs)
  - Explicitly abstracted components
  - No exact invariants, numerical thresholds, or attack-response logic

- **api_reference.md** - Surface-level API documentation
  - Function signatures and input/output types
  - Intended usage and docstrings
  - No parameter tuning guidance or performance-critical defaults

- **development_guide.md** - Contributor-focused guide
  - Installation and setup instructions
  - Coding standards and development workflows
  - How to add new experiments
  - No internal workflows or CI/CD credentials

- **testing_guide.md** - Reproducibility-oriented documentation
  - Test structure and organization
  - What tests validate (correctness, stability)
  - How to run tests
  - No stress limits or edge cases tied to adversarial behavior

- **config_reference.md** - Descriptive, not prescriptive
  - Parameter names, types, and units
  - High-level purpose of each parameter
  - No recommended values or threat-dependent tuning

- **troubleshooting.md** - Benign errors only
  - Import errors and environment setup issues
  - NaN handling explanations
  - Common Python mistakes
  - No failure recovery logic or attack-response procedures

### Private Documentation (docs_internal/ - excluded from GitHub)

Moved all private/strategic documentation to docs_internal/:

- Full system architecture with detailed diagrams and sequence charts
- Security documentation (threat models, defense strategies)
- Deployment & Operations (runtime configurations, deployment topologies)
- Internal API reference (non-public modules, experimental hooks)
- Release/Fork strategy documentation
- Grant/Internal fork templates and scripts
- Configuration defaults used in evaluation
- All operational and security-sensitive content

## Security Compliance

### .gitignore Updates

Explicitly exclude private documentation:
- `docs_internal/` directory
- `*.internal.md` files
- `*.restricted.md` files
- `deployment/` directory
- `security/` directory

### README Updates

- Added recommended disclaimer language:
  "This repository intentionally omits deployment, security, and operational
  documentation. Those materials are available under controlled access for
  research, evaluation, and funding purposes."

- Updated documentation links to point to public `docs/` folder
- Clear separation of what's included vs excluded
- Explicit documentation scope section

## Documentation Philosophy

**Public documentation explains:**
- How the system works (architecture, API)
- How to reproduce results (development, testing)
- How to extend it safely (development guide, configuration)

**Private documentation contains:**
- How to deploy it (deployment procedures)
- How to defend it (security architecture)
- How to tune it for adversarial conditions (operational configuration)

## Impact

### Security Benefits
- Protects operational details from public exposure
- Prevents revealing exact thresholds and security assumptions
- Maintains clear boundaries between public and private content
- Aligns with dual-use research best practices

### Research Benefits
- Maintains transparency for reproducibility
- Enables open collaboration on research aspects
- Protects sensitive operational information
- Signals responsible handling of dual-use technology

### Reviewer/Funder Benefits
- Demonstrates understanding of dual-use risks
- Shows responsible documentation practices
- Maintains research transparency
- Protects operational details appropriately

## File Structure

```
SMBNA/
├── docs/                    # Public documentation (committed)
│   ├── architecture_overview.md
│   ├── api_reference.md
│   ├── development_guide.md
│   ├── testing_guide.md
│   ├── config_reference.md
│   ├── troubleshooting.md
│   └── README.md
├── docs_internal/          # Private documentation (excluded)
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── SECURITY.md
│   ├── DEPLOYMENT_OPERATIONS.md
│   ├── API_REFERENCE.md (internal)
│   ├── RELEASE_STRATEGY.md
│   ├── FORK_STRATEGY.md
│   └── ... (all internal docs)
└── README.md               # Updated with disclaimer and links
```

## Compliance

This reorganization follows:
- Research lab best practices
- Defense contractor documentation standards
- Dual-use academic project guidelines
- Reviewer-approved documentation splits
- MIT license protection considerations

## Notes

- All public documentation is sanitized to remove operational details
- Private documentation remains available internally
- Clear boundaries established between public and private content
- Documentation structure is defensible and reviewer-friendly
- Maintains research transparency while protecting sensitive information

This reorganization establishes a professional, secure, and reviewer-friendly
documentation structure that protects operational details while maintaining
research transparency and reproducibility.
