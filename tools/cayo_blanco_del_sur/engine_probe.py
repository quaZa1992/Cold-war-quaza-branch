# IMPERIA COLD WAR — isolated native-engine island and transfer probe.
"""Own profile/fixture only. The user's launcher, saves and playset are untouched."""
from pathlib import Path
import argparse
import json
import subprocess
import time

from build import ROOT, HERE, AUDIT, STATE_ID, PROVINCE_ID, STATE_PATH, LOC_PATH

GAME = Path("E:/SteamLibrary/steamapps/common/Hearts of Iron IV")
PROFILE = HERE / "runtime/engine_profile"


def write(rel, text):
    p = PROFILE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hold", action="store_true", help="Keep the task-owned engine open after the probe for UI/save checks.")
    parser.add_argument("--load", help="An existing save basename in this isolated profile.")
    options = parser.parse_args()
    descriptor = (ROOT / "descriptor.mod").read_text(encoding="utf-8-sig") + '\npath="' + ROOT.as_posix() + '"\n'
    write("mod/mdcoldwar.mod", descriptor)
    addon = 'name="COLDWAR Cayo island probe"\ndependencies={ "MD Cold War" }\npath="' + (PROFILE / "fixture").as_posix() + '"\n'
    write("mod/cayo_probe.mod", addon)
    write("fixture/descriptor.mod", addon)
    write("dlc_load.json", json.dumps({"enabled_mods": ["mod/mdcoldwar.mod", "mod/cayo_probe.mod"], "disabled_dlcs": []}))
    write("settings.txt", 'language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    write("fixture/common/on_actions/zzzzzz_COLDWAR_cayo_probe.txt", '''# IMPERIA COLD WAR — isolated island verification hook.
on_actions = { on_startup = { effect = {
 log = "COLDWAR_CAYO_ENGINE STARTUP"
 CUB = { country_event = { id = COLDWAR_CAYO_ENGINE.1 hours = 1 } }
} } }
''')
    write("fixture/events/COLDWAR_cayo_probe.txt", '''# IMPERIA COLD WAR — diagnostic effects never shipped as live events.
add_namespace = COLDWAR_CAYO_ENGINE
country_event = { id = COLDWAR_CAYO_ENGINE.1 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { 1252 = { is_owned_and_controlled_by = CUB is_core_of = CUB NOT = { is_core_of = DDR } } }
  log = "COLDWAR_CAYO_ENGINE PASS initial_owner_core" }
 else = { log = "COLDWAR_CAYO_ENGINE FAIL initial_owner_core" }
 if = { limit = { 1252 = { check_variable = { productivity_state_var = 254.534 } check_variable = { building_level@industrial_complex = 0 } check_variable = { building_level@naval_base = 0 } } }
  log = "COLDWAR_CAYO_ENGINE PASS initial_economy" }
 else = { log = "COLDWAR_CAYO_ENGINE FAIL initial_economy" }
 1252 = { log = "COLDWAR_CAYO_ENGINE name=[This.GetName] population_k=[?state_population_k] productivity=[?productivity_state_var]" }
 log = "COLDWAR_CAYO_ENGINE cuba_gdp=[?gdp_total]"
 if = { limit = { check_variable = { gdp_total > 0 } } log = "COLDWAR_CAYO_ENGINE PASS cuba_gdp_positive" }
 else = { log = "COLDWAR_CAYO_ENGINE FAIL cuba_gdp_positive" }
 DDR = { transfer_state = 1252 }
 country_event = { id = COLDWAR_CAYO_ENGINE.2 hours = 1 }
} }
country_event = { id = COLDWAR_CAYO_ENGINE.2 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { 1252 = { is_owned_and_controlled_by = DDR is_core_of = CUB NOT = { is_core_of = DDR } } 854 = { is_owned_and_controlled_by = CUB } 1121 = { is_owned_and_controlled_by = CUB } 855 = { is_owned_and_controlled_by = CUB } }
  log = "COLDWAR_CAYO_ENGINE PASS isolated_ddr_transfer" }
 else = { log = "COLDWAR_CAYO_ENGINE FAIL isolated_ddr_transfer" }
 1252 = { set_state_name = COLDWAR_CUB_ernst_thaelmann_island_name }
 log = "COLDWAR_CAYO_ENGINE renamed=[1252.GetName]"
 CUB = { transfer_state = 1252 }
 1252 = { set_state_name = STATE_1252 }
 country_event = { id = COLDWAR_CAYO_ENGINE.3 hours = 1 }
} }
country_event = { id = COLDWAR_CAYO_ENGINE.3 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { 1252 = { is_owned_and_controlled_by = CUB is_core_of = CUB has_state_flag = COLDWAR_CUB_cayo_blanco_del_sur } }
  log = "COLDWAR_CAYO_ENGINE PASS returned_to_cuba" }
 else = { log = "COLDWAR_CAYO_ENGINE FAIL returned_to_cuba" }
 set_country_flag = COLDWAR_CAYO_ENGINE_complete
 log = "COLDWAR_CAYO_ENGINE COMPLETE"
} }
''')
    for name in ["game.log", "error.log"]:
        p = PROFILE / "logs" / name
        if p.exists():
            p.write_text("", encoding="utf-8")
    write("ui_release.txt", "pending\n")
    args = [str(GAME / "hoi4.exe"), "-debug", "-noasserts", "-assertsdialog=no", "-userdir=" + str(PROFILE)]
    if options.load:
        args += ["-load_file=" + options.load, "-start_speed=1"]
    else:
        args += ["-start_tag=CUB", "-start_speed=2", "-hands_off"]
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    started = time.time()
    process = subprocess.Popen(args, cwd=GAME, startupinfo=startup)
    write("process.json", json.dumps({"pid": process.pid, "args": args, "started": started}, indent=2))
    print(json.dumps({"pid": process.pid, "profile": str(PROFILE)}, indent=2), flush=True)
    game_log, error_log = PROFILE / "logs/game.log", PROFILE / "logs/error.log"
    complete = False
    interrupted = False
    try:
        while process.poll() is None and time.time() - started < 600:
            time.sleep(1)
            logs = game_log.read_text(encoding="utf-8-sig", errors="replace") if game_log.exists() else ""
            if "COLDWAR_CAYO_ENGINE COMPLETE" in logs or options.load:
                complete = "COLDWAR_CAYO_ENGINE COMPLETE" in logs
                if complete or (options.load and time.time() - started > 120):
                    break
        if options.hold and process.poll() is None:
            print(json.dumps({"ui_ready_pid": process.pid, "probe_complete": complete}), flush=True)
            until = time.monotonic() + 900
            while process.poll() is None and time.monotonic() < until:
                if (PROFILE / "ui_release.txt").read_text().strip() == "done":
                    break
                time.sleep(1)
    except KeyboardInterrupt:
        interrupted = True
    finally:
        stopped = process.poll() is None
        if stopped:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    logs = game_log.read_text(encoding="utf-8-sig", errors="replace") if game_log.exists() else ""
    errors = error_log.read_text(encoding="utf-8-sig", errors="replace") if error_log.exists() else ""
    expected = ["initial_owner_core", "initial_economy", "cuba_gdp_positive", "isolated_ddr_transfer", "returned_to_cuba"]
    relevant = [l for l in errors.splitlines() if any(s in l for s in ["COLDWAR_CAYO_ENGINE", "1252", "16537", "mdcw_cayo_blanco", "Cayo Blanco"])]
    report = {"scope": "Actual native engine with isolated profile and temporary probe events; UI and save/reload tracked separately.", "startup_reached": "COLDWAR_CAYO_ENGINE STARTUP" in logs, "completed": "COLDWAR_CAYO_ENGINE COMPLETE" in logs, "checkpoints": [l for l in logs.splitlines() if "COLDWAR_CAYO_ENGINE" in l], "relevant_errors": relevant, "returncode": process.returncode, "stopped_by_probe": stopped, "elapsed_seconds": round(time.time() - started, 1)}
    report["success"] = report["completed"] and all("COLDWAR_CAYO_ENGINE PASS " + name in logs for name in expected) and "COLDWAR_CAYO_ENGINE FAIL" not in logs and not relevant
    report["interrupted"] = interrupted
    (AUDIT / "engine_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
