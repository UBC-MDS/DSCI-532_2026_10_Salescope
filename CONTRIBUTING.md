# Contributing

Contributions of all kinds are welcome here, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

## Example Contributions

You can contribute in many ways, for example:

* [Report bugs](#report-bugs)
* [Fix Bugs](#fix-bugs)
* [Implement Features](#implement-features)
* [Write Documentation](#write-documentation)
* [Submit Feedback](#submit-feedback)

### Report Bugs

Report bugs at https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/issues.

**If you are reporting a bug, please follow the template guidelines. The more
detailed your report, the easier and thus faster we can help you.**

### Fix Bugs

Look through the GitHub issues for bugs. Anything labelled with `bug` and
`help wanted` is open to whoever wants to implement it. When you decide to work on such
an issue, please assign yourself to it and add a comment that you'll be working on that,
too. If you see another issue without the `help wanted` label, just post a comment, the
maintainers are usually happy for any support that they can get.

### Implement Features

Look through the GitHub issues for features. Anything labelled with
`enhancement` and `help wanted` is open to whoever wants to implement it. As
for [fixing bugs](#fix-bugs), please assign yourself to the issue and add a comment that
you'll be working on that, too. If another enhancement catches your fancy, but it
doesn't have the `help wanted` label, just post a comment, the maintainers are usually
happy for any support that they can get.

### Write Documentation

Salescope could always use more documentation, whether in the README,
docstrings, or in the `reports/` and `docs/` folders. Open an
[issue](https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/issues)
to let us know what you will be working on so we can align with the rest of the team.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/issues. If your feedback fits the format of one of
the issue templates, please use that. Remember that this is a volunteer-driven
project and everybody has limited time.

## Get Started!

Ready to contribute? Here's how to set up Salescope for local development.

1. Fork the [repository](https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope) on GitHub.
2. Clone your fork locally and create an environment (see the [README](README.md) for full steps):

    ```shell
    git clone https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope.git
    cd DSCI-532_2026_10_Salescope
    conda env create -f environment.yml
    conda activate Salescope
    ```

3. Create a branch from `dev` (or `main` for hotfixes). Use a short prefix like `fix/` or `feat/` and a descriptive name.

    ```shell
    git checkout dev
    git checkout -b fix/short-description-of-change
    ```

    Make your changes locally.

4. Run the test suite before pushing:

    ```shell
    python -m pytest -v
    ```

5. Commit with a clear message and push your branch. We use meaningful commit messages so that the history stays readable.

    ```shell
    git add .
    git commit -m "fix: brief description of what changed"
    git push -u origin fix/short-description-of-change
    ```

6. Open a pull request against `dev` and request a review. All PRs need at least one approval before merge.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. One logical change per PR (one feature or one fix). Keeps reviews focused and history clear.
2. If the PR adds functionality, update the docs (README, CHANGELOG, or spec) as needed.
3. Request at least one review; we do not merge without approval.
4. Run the test suite locally (`python -m pytest -v`) so it passes before requesting review.


## Attribution

This `CONTRIBUTING.md` document is adapted from cookiecutter at [https://cookiecutter.readthedocs.io/en/latest/CONTRIBUTING.html](https://cookiecutter.readthedocs.io/en/latest/CONTRIBUTING.html).

## M3 Reflection

Additional context is required on the M3 collaboration. The initial reflection of M1 and M2's collaboration was LLM-reported in the first revision of [Issue #107](https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/issues/107). At this time, there were a few issues observed summarised:


- There was an initial imbalance in which two people contributed a significant portion (about 80%) which risked inconsistent understandings of the codebase across all members.
- Some PRs had minimal review notes and consisted only of an approval and merge, with a few cases not having an approval before merge entirely.
- Documentation updates were mixed at times, there were PRs such as #71 and #76 where both feature and documentation were properly included while other cases such as #29 and #36 are fairly large PRs with no added documentation.
- None of the `src/app.py` code was modularized yet in M1 and M2 this was manageable .


This was the main decision for having the contributor with the most lines of code in M1 and M2 take more of a Project Manager role, in which his main task would be creating the issues needed to cover the M3 expectations. Additionally, since M3 was taking place during the quiz week, our group came to a mutual agreement to allow ourselves to focus entirely on the quizzes, with work on this milestone only expected to start on Friday. The exception to this was the Project Manager; since his quizzes were all on Tuesday, he could create the issues from Wednesday to Friday to allow for the implementation of M3's features to go more smoothly on Friday and Saturday. This alongside the other mentioned points above was our main process we aimed for when collaborating in M3.


### What Went Well


- In terms of the work done for M3, we accomplished past the issues we set ourselves to complete as expectation. Observing the [Kanban board at Milestone 3](https://github.com/orgs/UBC-MDS/projects/376/views/1?filterQuery=milestone%3A%22Milestone+3%22), a priority system was introduced for issues, in which `P0` indicated critical issues that needed to be resolved immediately, `P1` indicated important issues that were required for M3, and `P2` indicated issues that were nice to complete but had the expectation that may have been part of M4. In actuality, what we ended up accomplishing was all the issues with a labelled priority as well as several newly created issues that were meant for M4 finetuning not part of the original feedback.


- Assigning the person with the highest code contribution in M1 and M2 to the project manager role allowed the authorship concentration to balance out noticeably, creating a greater overall understanding of the codebase by each team member.


- Higher frequency and quality of discussion on average in the PRs. Nearly every PR had multiple comments, and there were increased edits post review for changes requested to ensure each PR was producing the best work possible.


- The CHANGELOG included the relevant issues for each point in this milestone, which made our update for M3 much more easily traceable and was a useful practice for organizing what requirements needed to be completed as we worked.


### What Could Have Been Improved


- Due to the ambitious scope of M3 and the strategic decision to focus nearly all of the work on Saturday, the deadline-eve burst proved to be extremely stressful and at times mistake prone, there were several PRs (#106, #111, #112, #136, #141) that were closed due to their work either being duplicates of other issues or having been already merged into other branches, resulting in some PRs violating the atomicity guideline.


- The increasing complexity of `src/app.py` in M3 eventually resulted in an 896 line long God Object. Even though there was reasonably clean code practices despite this code smell, it resulted in a higher than necessary number of merge conflicts to resolve.


- While the Project Manager role was mostly successful given the end result of M3, the inexperience was somewhat present as further issues that were not explicitly covered in the initial issues setup by Thursday had to be added on, making it difficult to estimate the scope of work remaining.


### Improvements Made for M4


M3 could best be described as a dramatic success overall, in that while the unintentional procrastination made the process on Saturday concerningly high paced, we were able to complete all the AI integration and several useful improvements to the dashboard with minimal bug concerns. Based on this reflection, we made the following improvements in our M4 collaboration process:


- Issue creation was more structured than in M3; a main issue in #151 was reintroduced with child issues being set up for each requirement. That meant we rarely had to spin up new issues mid-sprint—most work was already scoped.
- We spread work across the week instead of piling it onto the last day. Completing issues at a steadier pace gave us time for proper reviews and avoided the kind of deadline-eve rush we saw in M3.
- We refactored `src/app.py` by moving logic into `dflogic.py` and `db.py`, so the main app file is easier to follow and the filtering/aggregation logic is testable. Details are in the [CHANGELOG](CHANGELOG.md).

**Norms we committed to for M4:** one feature or fix per PR (no large dumps), design or spec updates before code for bigger changes, and every PR gets a review before merge. This CONTRIBUTING update was merged via [PR #209](https://github.com/UBC-MDS/DSCI-532_2026_10_Salescope/pull/209).
