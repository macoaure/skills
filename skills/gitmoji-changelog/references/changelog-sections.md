# Gitmoji → Changelog Section (gitmoji-changelog's own fixed mapping)

This is not something this skill invented — it's transcribed straight from `groupMapping.js`
inside the `gitmoji-changelog` package itself (v2.3.0). The CLI reads each commit's leading
`:shortcode:` (or the rendered emoji — it converts between the two internally) and sorts the
commit into exactly one of these Keep a Changelog–style sections, in this fixed order. There's
no way to influence this per-run short of a custom `.gitmoji-changelogrc` `commitMapping`
override; knowing it ahead of time means you can tell the user which section a commit will land
in before generating anything.

This is a **separate** mapping from the gitmoji-commits skill's conventional-commit type table —
the two tools group gitmoji for different purposes (changelog section vs. commit type), and they
don't always agree (e.g. `:boom:` is "feat" to gitmoji-commits but its own "Breaking changes"
section here). That's fine; neither mapping is wrong, they just answer different questions.

## Added

`:sparkles:` `:tada:` `:white_check_mark:` `:construction_worker:` `:chart_with_upwards_trend:`
`:heavy_plus_sign:` `:loud_sound:`

## Changed

`:art:` `:zap:` `:lipstick:` `:rotating_light:` `:arrow_down:` `:arrow_up:` `:pushpin:`
`:recycle:` `:wrench:` `:rewind:` `:alien:` `:truck:` `:bento:` `:wheelchair:` `:speech_balloon:`
`:card_file_box:` `:children_crossing:` `:building_construction:` `:iphone:`

## Breaking changes

`:boom:`

## Deprecated

(nothing mapped here by default — add one via `.gitmoji-changelogrc` if you want to use it)

## Removed

`:fire:` `:heavy_minus_sign:` `:mute:`

## Fixed

`:bug:` `:ambulance:` `:green_heart:` `:pencil2:`, plus four legacy platform-specific aliases
from older gitmoji catalog versions that may still show up in old history: `:apple:` `:penguin:`
`:checkered_flag:` `:robot:` `:green_apple:`

## Security

`:lock:`

## Useless — dropped from the changelog entirely

`:bookmark:` (release/version tag commits). These commits are filtered out before the changelog
is even built, not just hidden under a section — if a commit seems to be missing, check whether
it used this gitmoji.

## Miscellaneous

Everything else lands here — most of the gitmoji catalog isn't listed above (`:memo:`, `:label:`,
`:coffin:`, `:necktie:`, and so on all fall through to Misc). This is the safety net: no commit
with a recognized gitmoji silently disappears, it just lands here if it isn't one of the specific
ones sorted into a section above.
