from Backend.schemas import AnalysisResponse


def generate_markdown_report(result: AnalysisResponse, language: str, explanation_level: str) -> str:
    lines = [
        '# FixProof AI — Code Analysis Report', '',
        f'- **Language:** {language.title()}',
        f'- **Explanation level:** {explanation_level.title()}',
        '- **Execution status:** Code was not executed',
        f'- **Severity:** {result.severity.title()}',
        f'- **AI confidence:** {result.confidence}%', '',
        '## Summary', '', result.summary, '', '## Issues identified', ''
    ]
    lines.extend(f'- {item}' for item in result.issues) if result.issues else lines.append('No specific issues were identified.')
    lines.extend(['', '## Root cause', '', result.root_cause, '', '## Verification checklist', ''])
    lines.extend(f'- [ ] {step}' for step in result.verification_steps) if result.verification_steps else lines.append('- [ ] Review the changes and run relevant tests.')
    lines.extend(['', '## Suggested fixes', ''])
    if result.suggested_fixes:
        for i, fix in enumerate(result.suggested_fixes, 1):
            lines.extend([f'### {i}. {fix.title}', '', fix.explanation, '', '```', fix.code, '```', ''])
    else:
        lines.append('No specific fixes were suggested.')
    lines.extend(['', '## Suggested tests', ''])
    if result.tests:
        for i, test in enumerate(result.tests, 1):
            lines.extend([f'### Test {i}', '', test.description, '', '```', test.test_code, '```', ''])
    else:
        lines.append('No test suggestions were provided.')
    lines.extend(['', '## Limitations', ''])
    lines.extend(f'- {item}' for item in result.limitations) if result.limitations else lines.append('AI-generated findings have not been independently verified.')
    lines.extend(['', '---', 'AI confidence is an estimate, not a guarantee. Review changes and run tests before use.', ''])
    return '\n'.join(lines)
