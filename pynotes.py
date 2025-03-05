import math

# Given information
team_size = 12
pto_weeks_per_person = 5
weeks_per_year = 52
sprint_length = 2  # weeks
sprints_per_year = weeks_per_year / sprint_length  # 26 sprints per year

# Calculate total PTO weeks for the team
total_pto_weeks = team_size * pto_weeks_per_person
print(f"Total PTO weeks across the team in a year: {total_pto_weeks}")

# Calculate expected PTO weeks per sprint (uniformly distributed)
expected_pto_per_sprint = total_pto_weeks / sprints_per_year
print(f"Expected PTO weeks per sprint (uniform distribution): {expected_pto_per_sprint}")

# For a normal distribution, we need to consider how PTO might be spread
# We'll assume the mean PTO per sprint is the same as the uniform expectation
mean_pto_per_sprint = expected_pto_per_sprint

# For the standard deviation, we need to make an assumption
# If PTO is normally distributed across the year, we can estimate the standard deviation
# A reasonable assumption might be that 95% of sprints fall within ±50% of the mean
# For a normal distribution, 95% falls within ±1.96 standard deviations

# So if 1.96 * std_dev = 0.5 * mean, then:
std_dev = (0.5 * mean_pto_per_sprint) / 1.96
print(f"Estimated standard deviation for PTO per sprint: {std_dev}")

# Calculate confidence intervals
ci_90 = 1.645 * std_dev
ci_95 = 1.96 * std_dev
ci_99 = 2.576 * std_dev

print(f"90% Confidence Interval: {mean_pto_per_sprint - ci_90} to {mean_pto_per_sprint + ci_90} weeks")
print(f"95% Confidence Interval: {mean_pto_per_sprint - ci_95} to {mean_pto_per_sprint + ci_95} weeks")
print(f"99% Confidence Interval: {mean_pto_per_sprint - ci_99} to {mean_pto_per_sprint + ci_99} weeks")

# Express in person-days per sprint (assuming 5 workdays per week)
mean_pto_days_per_sprint = mean_pto_per_sprint * 5  # convert weeks to workdays
print(f"Expected PTO days per sprint: {mean_pto_days_per_sprint}")

ci_90_days = ci_90 * 5
ci_95_days = ci_95 * 5
ci_99_days = ci_99 * 5

print(f"90% CI in workdays: {mean_pto_days_per_sprint - ci_90_days} to {mean_pto_days_per_sprint + ci_90_days} days")
print(f"95% CI in workdays: {mean_pto_days_per_sprint - ci_95_days} to {mean_pto_days_per_sprint + ci_95_days} days")
print(f"99% CI in workdays: {mean_pto_days_per_sprint - ci_99_days} to {mean_pto_days_per_sprint + ci_99_days} days")
