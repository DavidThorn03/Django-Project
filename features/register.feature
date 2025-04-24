Feature: Register
  New Client want to register an account

  Scenario: Successfully register
    Given the user is in the register page
    When the user enters valid data and an email that isn’t in use
    And the user clicks on the register button
    Then the Client should be registered and directed to the login page

  Scenario: Invalid data entered
    Given the user is in the register page
    When the user enters invalid data
    And the user clicks on the register button
    Then the user should be informed that the data is invalid

  Scenario: Client account already exists
    Given the user is in the register page
    When the user enters valid data and an email that is already liked to an account
    And the user clicks on the register button
    Then the user should be informed that an account with this email already exists
