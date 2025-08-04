from how_to_use import print_running, A


a = A()
a.public()                          # Runs without warning and error            (uses print_running inside by the owner file)
a.protected()                       # Runs with printing protected warning      (uses print_running inside by the owner file)
print(50*'#')
a._A__private()                     # Raises _PrivateFunctionCalledException

print_running('how_to_use_2.py')    # Raises _PrivateFunctionCalledException    (‌Because this file is not the owner of the function)
