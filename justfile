year := "2022"
base_url := "https://adventofcode.com"

_default:
    @just --list --unsorted

# set up a reusable authenticated httpie session
auth session_cookie:
    poetry run http --session aoc "{{base_url}}" Cookie:session={{session_cookie}}

# get a day started
init day:
    #!/usr/bin/env bash
    url="{{base_url}}/{{year}}/day/{{day}}/input"
    destdir="{{year}}/$(printf %.2d {{day}})"
    inputfile="${destdir}/input"
    if [[ ! -d "${destdir}" ]]; then
        mkdir -p "${destdir}"
        touch "${destdir}/__main__.py"
    fi
    [[ -s "${inputfile}" ]] || poetry run http --session aoc --download --output "${inputfile}" "${url}"

# format code and run basic checks (default: all of current year)
lint day="":
    #!/usr/bin/env bash
    path="{{year}}"
    [[ -n "{{day}}" ]] && path="${path}/$(printf %.2d {{day}})"
    git ls-files -- "${path}" | xargs poetry run pre-commit run --files

# run the code for a day
run day input="input":
    #!/usr/bin/env bash
    dir="{{year}}/$(printf %.2d {{day}})"
    echo "Running $dir..."
    poetry run python "$dir" < "$dir/{{input}}"

run_vd day part:
    #!/usr/bin/env bash
    cd "{{year}}/$(printf %.2d {{day}})"
    poetry run vd \
        --visidata-dir=../../.visidata \
        --config=/dev/null \
        --batch \
        --play part{{part}}.vdj
