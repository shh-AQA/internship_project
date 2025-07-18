# Created by szhuss at 7/16/25
Feature: Tests for Secondary Listings page

Scenario: Filter Secondary deals by Unit price range (1200000 - 2000000 AED)
  Given the user opens the Reelly main page
  And the user logs into the page
  When the user clicks on the "Secondary" option in the left menu
  Then the Secondary page should open
  When the user clicks on the Filters button
  And sets the price range from 1200000 to 2000000 AED
  Then all displayed cards should have prices within that range
