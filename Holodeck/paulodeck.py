from Holodeck.holodeck_controller import JarvisHolodeck

if __name__ == "__main__":
  deck = JarvisHolodeck()
  deck.begin()

  # Test to see what the deck does
  print deck.handle({'tundra': True})

  raw_input("Enter to exit:")

