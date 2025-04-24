Feature: Login
  User wants to log in

  Scenario: Successfully login
    Given the user is in the login page
    When the user enters a valid email and password
    And clicks login
    Then the user should be redirected to the home page

  Scenario: Mismatched data entered
    Given the user is in the login page
    When the user enters a email and password that do not match
    And clicks login
    Then the user should be told their email and password are incorrect

  Scenario: Unknown data entered
    Given the user is in the login page
    When the user enters a email and password that aren’t in the system
    And clicks login
    Then the user should be told the user doesn’t exist
