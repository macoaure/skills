# Gitmoji → Conventional Commit Type (fixed mapping)

Source catalog: https://gitmoji.dev (75 entries, fetched from the official `gitmoji.dev/api/gitmojis` feed).

Each gitmoji has exactly one assigned conventional-commit type below. This is fixed on purpose:
several gitmoji could plausibly fit more than one type (`:zap:` could read as "fix" or "perf";
`:truck:` could read as "chore" or "refactor"), and if the type floated per-commit, the same
kind of change would get labeled differently from one commit to the next. Pin it once here so
every commit that uses a given gitmoji always gets the same type, and `scripts/validate_commit.py`
can check a message against this table mechanically.

Always write the shortcode as plain text (`:sparkles:`), never the rendered emoji character.
The shortcode is already gitmoji's own convention — GitHub, GitLab, and most git tooling render
`:sparkles:` as ✨ automatically in their UI, so nothing is lost, and the raw commit message
stays plain ASCII that's safe to grep, diff, and read in any terminal encoding.

Rows are grouped by type for quick scanning; the grouping is purely for this document's
readability and carries no meaning beyond the type column itself.

## feat

| Shortcode | Name | Description |
|---|---|---|
| `:sparkles:` | sparkles | Introduce new features. |
| `:chart_with_upwards_trend:` | chart-with-upwards-trend | Add or update analytics or track code. |
| `:globe_with_meridians:` | globe-with-meridians | Internationalization and localization. |
| `:boom:` | boom | Introduce breaking changes. |
| `:wheelchair:` | wheelchair | Improve accessibility. |
| `:card_file_box:` | card-file-box | Perform database related changes. |
| `:children_crossing:` | children-crossing | Improve user experience / usability. |
| `:iphone:` | iphone | Work on responsive design. |
| `:egg:` | egg | Add or update an easter egg. |
| `:mag:` | mag | Improve SEO. |
| `:triangular_flag_on_post:` | triangular-flag-on-post | Add, update, or remove feature flags. |
| `:dizzy:` | dizzy | Add or update animations and transitions. |
| `:passport_control:` | passport-control | Work on code related to authorization, roles and permissions. |
| `:necktie:` | necktie | Add or update business logic. |
| `:stethoscope:` | stethoscope | Add or update healthcheck. |
| `:thread:` | thread | Add or update code related to multithreading or concurrency. |
| `:safety_vest:` | safety-vest | Add or update code related to validation. |
| `:airplane:` | airplane | Improve offline support. |
| `:t-rex:` | t-rex | Code that adds backwards compatibility. |

## fix

| Shortcode | Name | Description |
|---|---|---|
| `:bug:` | bug | Fix a bug. |
| `:ambulance:` | ambulance | Critical hotfix. |
| `:lock:` | lock | Fix security or privacy issues. |
| `:rotating_light:` | rotating-light | Fix compiler / linter warnings. |
| `:green_heart:` | green-heart | Fix CI Build. |
| `:pencil2:` | pencil2 | Fix typos. |
| `:alien:` | alien | Update code due to external API changes. |
| `:speech_balloon:` | speech-balloon | Add or update text and literals. |
| `:goal_net:` | goal-net | Catch errors. |
| `:adhesive_bandage:` | adhesive-bandage | Simple fix for a non-critical issue. |

## docs

| Shortcode | Name | Description |
|---|---|---|
| `:memo:` | memo | Add or update documentation. |
| `:page_facing_up:` | page-facing-up | Add or update license. |
| `:bulb:` | bulb | Add or update comments in source code. |
| `:busts_in_silhouette:` | busts-in-silhouette | Add or update contributor(s). |

## style

| Shortcode | Name | Description |
|---|---|---|
| `:art:` | art | Improve structure / format of the code. |
| `:lipstick:` | lipstick | Add or update the UI and style files. |

## refactor

| Shortcode | Name | Description |
|---|---|---|
| `:recycle:` | recycle | Refactor code. |
| `:truck:` | truck | Move or rename resources (e.g.: files, paths, routes). |
| `:building_construction:` | building-construction | Make architectural changes. |
| `:label:` | label | Add or update types. |

## perf

| Shortcode | Name | Description |
|---|---|---|
| `:zap:` | zap | Improve performance. |

## test

| Shortcode | Name | Description |
|---|---|---|
| `:white_check_mark:` | white-check-mark | Add, update, or pass tests. |
| `:clown_face:` | clown-face | Mock things. |
| `:camera_flash:` | camera-flash | Add or update snapshots. |
| `:test_tube:` | test-tube | Add a failing test. |

## build

| Shortcode | Name | Description |
|---|---|---|
| `:arrow_down:` | arrow-down | Downgrade dependencies. |
| `:arrow_up:` | arrow-up | Upgrade dependencies. |
| `:pushpin:` | pushpin | Pin dependencies to specific versions. |
| `:heavy_plus_sign:` | heavy-plus-sign | Add a dependency. |
| `:heavy_minus_sign:` | heavy-minus-sign | Remove a dependency. |
| `:package:` | package | Add or update compiled files or packages. |
| `:bricks:` | bricks | Infrastructure related changes. |

## ci

| Shortcode | Name | Description |
|---|---|---|
| `:construction_worker:` | construction-worker | Add or update CI build system. |

## revert

| Shortcode | Name | Description |
|---|---|---|
| `:rewind:` | rewind | Revert changes. |

## chore

Housekeeping with no user-facing behavior change — this is the catch-all for gitmoji whose
description names an activity rather than an effect (deploying, merging, experimenting,
removing logs, etc.).

| Shortcode | Name | Description |
|---|---|---|
| `:fire:` | fire | Remove code or files. |
| `:rocket:` | rocket | Deploy stuff. |
| `:tada:` | tada | Begin a project. |
| `:closed_lock_with_key:` | closed-lock-with-key | Add or update secrets. |
| `:bookmark:` | bookmark | Release / Version tags. |
| `:construction:` | construction | Work in progress. |
| `:wrench:` | wrench | Add or update configuration files. |
| `:hammer:` | hammer | Add or update development scripts. |
| `:poop:` | poop | Write bad code that needs to be improved. |
| `:twisted_rightwards_arrows:` | twisted-rightwards-arrows | Merge branches. |
| `:bento:` | bento | Add or update assets. |
| `:beers:` | beers | Write code drunkenly. |
| `:loud_sound:` | loud-sound | Add or update logs. |
| `:mute:` | mute | Remove logs. |
| `:see_no_evil:` | see-no-evil | Add or update a .gitignore file. |
| `:alembic:` | alembic | Perform experiments. |
| `:seedling:` | seedling | Add or update seed files. |
| `:wastebasket:` | wastebasket | Deprecate code that needs to be cleaned up. |
| `:monocle_face:` | monocle-face | Data exploration/inspection. |
| `:coffin:` | coffin | Remove dead code. |
| `:technologist:` | technologist | Improve developer experience. |
| `:money_with_wings:` | money-with-wings | Add sponsorships or money related infrastructure. |
