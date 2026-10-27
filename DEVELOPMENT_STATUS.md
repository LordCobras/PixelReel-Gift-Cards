# PixelReel Gift Cards — development status

This project targets OpenCart 4.1.0.4, PHP 8.3, EUR, English, DC Toys and CatCode One Page Checkout.

Planned: Classic / Gaming / Retro designs, gift card PDF, email fulfillment and one-time redemption with no remaining balance.

**NOT PRODUCTION READY.** The v0.2 local prototype supports only basic administration and draft codes, without checkout redemption or customer issuance. Do not accept payments for gift cards using this prototype.

## OpenCart extension naming

OpenCart 4 extension package filename determines the extension code. The source namespace and route must match it. For the current source code the installer filename must be exactly `pixelgift_clean.ocmod.zip`, not a renamed version.

## Next steps

Import and review the source files from the tested prototype, implement payment fulfillment and safe redemption, add PDF and email output, and test installation and checkout in a staging shop before publishing any production ZIP.
