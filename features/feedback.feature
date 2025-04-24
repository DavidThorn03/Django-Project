Feature: Give Feedback
  A staff user wants to give feedback to a query

  Scenario: Successfully give feedback
    Given a user is logged in as staff
    And is in the query page
    When the user enters the feedback info
    And selects submit
    Then the feedback should be saved and sent as an email to the user
    And the staff should be informed of success

  Scenario: User not logged in as staff
    Given a user is logged in as staff
    And with the wrong hotel
    And is in the query page
    When the user enters the feedback info
    And selects submit
    Then the user should be redirected to the login page

  Scenario: The query has been replied to
    Given a user is logged in as staff
    And is in the query page
    When the user enters the feedback info
    And selects submit
    Then the staff member should be informed that this query has already been responded to
