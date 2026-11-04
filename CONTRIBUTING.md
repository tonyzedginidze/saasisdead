<p align="center"><img src="assets/art/contribute.svg" width="100%" alt="The reaper hands over a pull request"></p>

# Contributing

Thanks for helping people stop paying for software they can host or run themselves. Every entry is reviewed by hand, and accepted projects are added to [saasisdead.si](https://saasisdead.si) too.

## What gets in

A project is listed when all of these hold:

- **It replaces a paid product.** Name the SaaS or paid app it's an alternative to.
- **It is open source.** An OSI license, or a clearly marked source-available license (fair-code, Elastic, BSL). No license means no listing.
- **People use it.** At least 1,000 GitHub stars, or at least 500 when the repository is less than a year old.
- **It is alive.** Not archived, with commits in the last nine months.
- **It is what it says.** No crypto bait, star farming or descriptions we can't read.

## Add a project

1. Find the category, then the paid product your project replaces. Products are `###` headings inside each category.
2. Add one bullet, in alphabetical order:

   ```markdown
   - [Name](https://github.com/owner/repo) - What it does, in one plain sentence.
   ```

   If it replaces more than one product, list it under the main one and end the line with `Also replaces Product, Other Product.`
3. If the paid product is missing, add a `### Product` heading in the right category, in alphabetical order. A product logo is welcome but optional; maintainers add one otherwise.
4. Open a pull request with one project per pull request.

You can do all of this in the browser: [edit the README](https://github.com/tonyzedginidze/saasisdead/edit/main/README.md) and GitHub creates the fork and pull request for you.

## No time for a pull request?

[Suggest a project](https://github.com/tonyzedginidze/saasisdead/issues/new?template=suggest-project.yml) with a short form instead.

## Fixes

Dead links, wrong descriptions and archived projects are welcome fixes too. Open a pull request or an issue.
