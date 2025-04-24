Feature: Book Room
  Client wants to book a hotel room

  Scenario: Successfully book
    Given user has selected room
    When client enters check in and check out date
    And is logged in
    And selects book
    Then booking should be made and user should be brought to profile page

  Scenario: Invalid dates
    Given user has selected room
    When client enters invalid check in and check out date
    And is logged in
    And selects book
    Then the user should be informed that the dates are invalid

  Scenario: Not logged in as client
    Given user has selected room
    When the user is not logged in
    And client enters check in and check out date
    And selects book
    Then user should be redirected to login
