Feature: Make Query
  A client wants to make a query

  Scenario: Successfully make query
    Given the user is in the contact page
    When the user enters their query
    And selects submit query
    Then the query should be made
    And the user should be informed

  Scenario: User not logged in as client
    Given the user is in the contact page
    And isn’t logged in as client
    When the user enters their query
    And selects submit query
    Then the user should be redirected to login
