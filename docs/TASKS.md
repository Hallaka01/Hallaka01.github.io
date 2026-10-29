# Task board

- [x] T-01: Confirm the Neon City direction, static scope, and GitHub Pages destination.
- [x] T-02: Build the responsive portfolio, background artwork, project sections, and navigation.
- [x] T-03: Check content, accessibility, assets, and mobile and desktop behavior.
- [x] T-04: Publish through GitHub Pages and verify the live site.
- [x] T-05: Link the portfolio from the GitHub profile and record the final state.
- [x] T-06: Add stable project anchors for direct links from the profile and project showcase.
- [~] T-07: Make the website the full profile destination, remove generic profile-return calls to action, and keep direct project resources.

Validation: just check and four HTTP smoke tests passed. Browser checks covered desktop, narrow mobile (321 CSS pixels), image loading, section navigation, menu links, Escape/focus behavior, and the custom 404 page. No horizontal overflow was observed.

Published at https://hallaka01.github.io/ through the successful GitHub Actions workflow 40913042848. HTTPS is enforced; the home page returns 200 and unknown routes return the custom 404. The live browser loaded the project screenshots without console warnings or errors. The profile README and website field link to the portfolio.

T-06 validation: static checks and four HTTP tests pass; deployment 40916393596 succeeded. Live profile clicks reach the visible YGO Scanner and HSMWmobil cards through #ygo-scanner and #hsmwmobil.
