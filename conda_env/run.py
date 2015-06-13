from subprocess import call

def env_run(environment, program, arguments):
    activate_env = "source activate %s; " % environment
    command = activate_env + program + ' ' + ' '.join(arguments)
    print("Executing: " + command)
    call(command, shell=True)