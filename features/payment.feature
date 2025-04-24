Feature: Pay for booking
  A client wants to pay for their booking

  Scenario: Successfully pay
    Given user is in pay page
    And is logged in as client
    When user enters correct card information
    And selects pay
    Then booking should be set as paid
    And user should be told

  Scenario: Invalid card information
    Given user is in pay page
    And is logged in as client
    When user enters incorrect card information
    And selects pay
    Then the user should be informed that card information is invalid

  Scenario: User not logged in to correct client account
    Given user is in pay page
    And the user isnt logged in as client
    When user enters correct card information
    And selects pay
    Then the user should be redirected to login page
