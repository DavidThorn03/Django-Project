Feature: Leave rating
  Client wants to leave hotel review

  Scenario: Successfully make first rating
    Given the user is logged in as client
    And is on the hotel page
    When the user selects the rating they want to give
    Then the rating should be saved
    And the user should be informed

  Scenario: Successfully update rating
    Given the user is logged in as client
    And is on the hotel page
    And has already rated the hotel
    When the user selects the rating they want to give
    Then their rating of that hotel should be updated
    And the user should be informed

  Scenario: User is not logged in
    Given the user is not logged in
    And is on the hotel page
    When the user selects the rating they want to give
    Then they are redirected to the login page
