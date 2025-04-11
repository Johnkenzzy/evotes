-- ORGANIZATIONS
INSERT INTO organizations_organization (id, name, email, created_at, updated_at, password)
VALUES 
('00000000-0000-0000-0000-000000000001', 'TechVote Inc.', 'techvote@inc.com', NOW(), NOW(), 'hashedpassword1'),
('00000000-0000-0000-0000-000000000002', 'CivicElect Inc.', 'civicelect@inc.com', NOW(), NOW(), 'hashedpassword2');

-- ORGANIZATION ADMINS
INSERT INTO organizations_organizationadmin (id, organization_id, full_name, email, password, created_at, updated_at)
VALUES 
('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'Alice Admin', 'alice@techvote.com', 'hashedpassword1', NOW(), NOW()),
('10000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002', 'Bob Admin', 'bob@civicelect.com', 'hashedpassword2', NOW(), NOW());

-- ELECTIONS
INSERT INTO elections_election (id, organisation_id, name, title, start_time, end_time, is_active, created_at, updated_at)
VALUES 
('20000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'TechVote 2025', 'Board Elections 2025', NOW(), NOW() + interval '7 days', true, NOW(), NOW()),
('20000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002', 'CivicElect 2025', 'Leadership Elections 2025', NOW(), NOW() + interval '5 days', true, NOW(), NOW());

-- BALLOTS
INSERT INTO ballots_ballot (id, election_id, title, description, start_date, end_date, votes, created_at, updated_at)
VALUES 
('30000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'President', 'Vote for President', NOW(), NOW() + interval '7 days', 0, NOW(), NOW()),
('30000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000002', 'Chairperson', 'Vote for Chairperson', NOW(), NOW() + interval '5 days', 0, NOW(), NOW());

-- OPTIONS
INSERT INTO ballots_option (id, ballot_id, name, title, photo, votes, created_at, updated_at)
VALUES 
('40000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', 'Jane Doe', 'CTO at TechCorp', NULL, 0, NOW(), NOW()),
('40000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001', 'John Smith', 'Lead Engineer', NULL, 0, NOW(), NOW()),
('40000000-0000-0000-0000-000000000003', '30000000-0000-0000-0000-000000000002', 'Emily Rose', 'Professor of Political Science', NULL, 0, NOW(), NOW()),
('40000000-0000-0000-0000-000000000004', '30000000-0000-0000-0000-000000000002', 'Daniel Craig', 'Community Leader', NULL, 0, NOW(), NOW());

-- VOTERS
INSERT INTO voters_voter (id, organisation_id, voter_id, full_name, email, is_accredited, has_voted, created_at, updated_at)
VALUES 
('50000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'TV12345', 'Victor Voter', 'victor@voters.com', true, false, NOW(), NOW()),
('50000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001', 'TV12346', 'Valerie Vote', 'valerie@voters.com', true, false, NOW(), NOW()),
('50000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000002', 'CE12345', 'Charlie Civic', 'charlie@civic.com', true, false, NOW(), NOW());

-- VOTES
INSERT INTO voters_vote (id, voter_id, ballot_id, option_id, created_at, updated_at)
VALUES 
('60000000-0000-0000-0000-000000000001', '50000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000001', NOW(), NOW()),
('60000000-0000-0000-0000-000000000002', '50000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000002', NOW(), NOW()),
('60000000-0000-0000-0000-000000000003', '50000000-0000-0000-0000-000000000003', '30000000-0000-0000-0000-000000000002', '40000000-0000-0000-0000-000000000003', NOW(), NOW());

