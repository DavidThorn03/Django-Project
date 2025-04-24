Feature: Update hotel
  Web admin wants to update the hotel information

  Scenario: Successfully update info
    Given the user is logged in as web admin
    And is on hotel page
    When the user selects the field they want to change
    And enters the change
    And selects save
    Then the change should be saved the user should be informed

  Scenario: Failed with insufficient privilege
    Given the user is logged in as web admin 
    And does not have permission to update hotel info
    And is on hotel page
    When the user selects the field they want to change
    Then the user should be directed to the login page
