from Holodeck.holodeck_controller import JarvisHolodeck

if __name__ == "__main__":
  deck = JarvisHolodeck()

  # Test to see what the deck does
  print deck.handle({'beach': True})

  raw_input("Enter to exit:")

