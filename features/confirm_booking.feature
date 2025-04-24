Feature: Confirm/deny booking
  Staff wants to confirm/deny booking

  Scenario: Successfully confirm
    Given staff is viewing booking
    And is logged in as staff
    When staff selects to approve booking
    Then the booking should be approved
    And the staff should be informed

  Scenario: Successfully deny
    Given staff is viewing booking
    And is logged in as staff
    When staff selects to deny booking
    Then the booking should be removed
    And the staff should be informed

  Scenario: Not logged in as staff at hotel of booking
    Given staff is viewing booking
    When staff selects to approve booking
    And not logged in
    Then staff should be redirected to login
