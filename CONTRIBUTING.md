## Contributing

First off, thank you for considering contributing to Codedigger Backend API. It's people
like you that make Codedigger such a great website.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

This project and everyone participating in it is governed by the [Codedigger Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to contact.codedigger@gmail.com.

### Where do I go from here?

If you've noticed a bug or have a feature request, [make one][new issue]! It's
generally best if you get confirmation of your bug or approval for your feature
request this way before starting to code.

#### How to file an issue!

To make it easier to triage, we have these issue requirements:

* Please do your best to search for duplicate issues before filing a new issue so we can keep our issue board clean.
* Every issue should have **exactly** one bug/feature request described in it. Please do not file meta feedback list tickets as it is difficult to parse them and address their individual points.
* Feature Requests are better when they’re open-ended instead of demanding a specific solution -ie  “I want an easier way to do X” instead of “add Y”
* Issues are not the place to go off topic or debate.
* Please always remember our [privacy policy](https://codedigger.tech/privacy) and [terms](https://codedigger.tech/terms).
* Please do not tag specific team members to try to get your issue looked at faster. We have a triage process that will tag and label issues correctly in due time. If you think an issue is very severe, you can ask about it by contacting us.

If you have a general question about codedigger, contact us contact.codedigger@gmail.com or [join][discord link]! our discord community. 

Beginners! - Watch out for Issues with the ["Good First Issue"][good first issue]! label. These are easy bugs that have been left for first timers to have a go, get involved and make a positive contribution to the project!

You can learn from this free series, [How to Contribute to an Open Source Project on GitHub][open-source-tutorial]!.

### Fork & create a branch

If this is something you think you can fix, then [fork Codedigger Backend] and create
a branch with a descriptive name.

A good branch name would be : 
```sh
git checkout -b feature/AmazingFeature
```
```sh
git checkout -b bugfix/user
```

### Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help;
everyone is a beginner at first :smile_cat:

### Make a Pull Request

At this point, you should switch back to your master branch and make sure it's
up to date with Codedigger's master branch:

```sh
git remote add upstream git@github.com:Code-dig-ger/Backend.git
git checkout master
git pull upstream master
```

Then update your feature branch from your local copy of master, and push it!

```sh
git checkout feature/AmazingFeature
git rebase master
git push --set-upstream origin feature/AmazingFeature
```

Finally, go to GitHub and [make a Pull Request][] :D

### Keeping your Pull Request updated

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code
has changed, and that you need to update your branch so it's easier to merge.

To learn more about rebasing in Git, there are a lot of [good][git rebasing]
[resources][interactive rebase] but here's the suggested workflow:

```sh
git checkout feature/AmazingFeature
git pull --rebase upstream master
git push --force-with-lease feature/AmazingFeature
```

### PR requirements
To make it easier to review, we have these PR requirements:

* Every PR must have **exactly** one issue associated with it.
* Write a clear explanation of what the code is doing when opening the pull request, and optionally add comments to the PR.
* Keep PRs small and to the point. For extra code-health changes, either file a separate issue, or make it a separate PR that can be easily reviewed.
* Use micro-commits. This makes it easier and faster to review.

As You can keep your PRs small, it helps our team review and merge code faster, minimizing stale code.

PRs may take time to merge depending on the issue you are addressing. If you think your issue/PR is very important, try to popularize it by getting other users to comment and share their point of view.

### Merging a PR (maintainers only)

A PR can only be merged into master by a maintainer if:

* It is passing CI.
* It has been approved by at least two maintainers. If it was a maintainer who
  opened the PR, only one extra approval is needed.
* It has no requested changes.
* It is up to date with current master.

Any maintainer is allowed to merge a PR if all of these conditions are
met.

### Note

Please keep in mind that even though a feature you have in mind may seem like a small task, as a small team, we have to prioritize our planned work and every new feature adds complexity and maintenance and may take up design, research, marketing, product, and engineering time. That being said, just because we haven't replied, doesn't mean we don't care about the issue, please be patient with our response times as we're very busy.


[new issue]: https://github.com/Code-dig-ger/Backend/issues/new/choose
[discord link]: https://discord.gg/4ZeNgUn7cF
[good first issue]: https://github.com/Code-dig-ger/Backend/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22
[fork Codedigger Backend]: https://help.github.com/articles/fork-a-repo
[open-source-tutorial]: https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github
[make a pull request]: https://help.github.com/articles/creating-a-pull-request
[git rebasing]: http://git-scm.com/book/en/Git-Branching-Rebasing
[interactive rebase]: https://help.github.com/en/github/using-git/about-git-rebase