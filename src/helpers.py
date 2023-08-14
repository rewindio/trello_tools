def press_enter_to_continue():
  input("\nPress Enter to continue...")
  print("\n")

def prompt_y_n(prompt):
  resp = input(f"\n{prompt} (y/n): ").lower().strip()
  if resp == 'y':
    return True
  elif resp == 'n':
    return False
  else:
    print("Invalid input. Please try again.")
    return self.__prompt_y_n(prompt)

def prompt_for_number(num_choices):
  resp = input(f"\nEnter your choice: ")
  num = int(resp.strip())
  if num < 1 or num > num_choices:
    print("Invalid input. Please try again.")
    return self.__prompt_for_number(num_choices)
  return num
