# Architecture

## Stack

Buildless HTML, CSS, and a small deferred JavaScript file. Python provides local checks and preview; Node checks JavaScript syntax. No runtime packages, fonts, tracking scripts, API calls, or backend services are required.

## Structure

- site/index.html: semantic content and navigation.
- site/styles/: design tokens, layout, components, and responsive rules.
- site/scripts/main.js: mobile navigation and optional progressive enhancements.
- site/assets/: original city artwork and fictional app demo screenshots.
- scripts/ and tests/: static checks and an HTTP smoke test.

Critical content and links work without JavaScript. Enhancements honor reduced-motion preferences. Images have fixed dimensions and meaningful alternatives; missing images leave the associated text and links usable.

The stable fragment destinations #work, #about, #ygo-scanner, and #hsmwmobil let profile and showcase links open the relevant content directly.

## Delivery

Just is the universal command interface. Lefthook checks commits and pushes. GitHub Actions checks the site and publishes only the site directory through the official Pages actions. The GitHub profile and its existing repository remain separate.
