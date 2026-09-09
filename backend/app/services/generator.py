import re

def generate_test_cases(description: str) -> dict[str, list[str]]:
    description_lower = description.lower()

    result = {
        "positive": [],
        "negative": [],
        "edge_cases": [],
        "security": [],
    }

    login_keywords = [
        "login",
        "log in",
        "password",
        "email",
        "e-mail",
    ]

    if any(word in description_lower for word in login_keywords):
        # More comprehensive login-related suggestions covering UX, security, and integrations
        result["positive"] = [
            "Login with valid email and password",
            "Login with username instead of email (if supported)",
            "Login with remembered device (remember-me) preserves session",
            "Login via single-sign-on (SSO) / OAuth provider succeeds",
            "Login succeeds with valid MFA (TOTP/Email/SMS) when enabled",
        ]

        result["negative"] = [
            "Login fails with incorrect password",
            "Login fails with unknown email address",
            "Login fails when password is empty",
            "Login fails when email/username is empty",
            "Login fails when MFA token is invalid or expired",
            "Login is rejected for locked or disabled accounts",
        ]

        result["edge_cases"] = [
            "Email/username with maximum allowed length",
            "Password with special characters and unicode characters",
            "Email with leading and trailing spaces",
            "Login with very long password and very short password",
            "Session timeout and auto-logout after inactivity",
            "Remember-me cookie expiry and revocation",
        ]

        result["security"] = [
            "SQL injection attempt in email/username field is rejected",
            "Cross-site scripting payload in login form is sanitized",
            "Brute-force protection and rate-limiting after multiple failed attempts",
            "Account lockout and unlock workflows are enforced",
            "Password reset flow prevents account takeover (token expiry, single-use)",
            "Session cookie flags (HttpOnly, Secure, SameSite) are set",
            "Ensure no sensitive data (passwords, tokens) are logged",
            "Login does not leak whether an account exists (prevents enumeration), unless explicitly allowed",
        ]

    else:
        # Tokenize description to detect likely actions or domains and improve fallback suggestions
        tokens = set(re.findall(r"\w+", description_lower))

        suggestions_positive = [
            "Function works with valid input",
        ]

        suggestions_negative = [
            "System rejects invalid input",
        ]

        suggestions_edge = [
            "System handles empty input correctly",
            "System handles boundary values correctly",
        ]

        suggestions_security = [
            "Input validation prevents malicious payloads",
        ]

        # Action/domain-specific heuristics
        if tokens & {"create", "add", "register", "signup", "insert"}:
            suggestions_positive.extend([
                "Successfully creates resource with valid payload",
                "Response contains created resource ID",
            ])
            suggestions_negative.extend([
                "Creation fails with missing required fields",
                "Creation fails with duplicate unique field",
            ])
            suggestions_edge.extend([
                "Creation with very large payload",
                "Creation with only optional fields provided",
            ])

        if tokens & {"update", "edit", "modify", "patch"}:
            suggestions_positive.extend([
                "Updates resource with valid changes",
                "Partial update (PATCH) works as expected",
            ])
            suggestions_negative.extend([
                "Update fails when resource not found",
                "Update rejects invalid field types",
            ])
            suggestions_edge.extend([
                "Concurrent updates are handled consistently",
                "Update with unchanged payload is idempotent",
            ])

        if tokens & {"delete", "remove", "destroy"}:
            suggestions_positive.extend([
                "Deletes existing resource and returns expected status",
            ])
            suggestions_negative.extend([
                "Delete fails for non-existent resource",
                "Delete is forbidden without proper permission",
            ])
            suggestions_edge.extend([
                "Repeated delete is idempotent",
                "Delete while resource is in active use",
            ])

        if tokens & {"list", "get", "fetch", "search", "query"}:
            suggestions_positive.extend([
                "Returns list of resources matching filters",
                "Pagination returns correct counts and pages",
            ])
            suggestions_negative.extend([
                "Invalid filter parameter returns an error or is ignored",
            ])
            suggestions_edge.extend([
                "Pagination boundary (page size=1 & beyond last page)",
                "Performance with very large result sets",
            ])

        if tokens & {"upload", "file", "image", "attachment"}:
            suggestions_positive.extend([
                "File uploads succeed for allowed types",
            ])
            suggestions_negative.extend([
                "Rejects disallowed file types and oversized files",
            ])
            suggestions_edge.extend([
                "Filename with unicode and special characters",
                "Very large file upload behavior (timeout, chunking)",
            ])
            suggestions_security.extend([
                "Path traversal in filename is prevented",
                "File type spoofing is detected and rejected",
            ])

        if tokens & {"payment", "pay", "transaction", "checkout"}:
            suggestions_positive.extend([
                "Successful payment with valid payment method",
            ])
            suggestions_negative.extend([
                "Payment declines handled gracefully and reported",
            ])
            suggestions_edge.extend([
                "Concurrent submissions do not double-charge",
                "Payment with different currencies",
            ])
            suggestions_security.extend([
                "Sensitive payment data is not logged",
                "Idempotency and replay protection for payment requests",
            ])

        if tokens & {"date", "time", "timezone", "dst", "leap"}:
            suggestions_edge.extend([
                "Handles daylight saving transitions correctly",
                "Handles leap-year and leap-second dates",
                "Timezone conversions produce expected results",
            ])

        if tokens & {"sort", "filter", "order"}:
            suggestions_positive.extend([
                "Sorting and filtering return correct order and subset",
            ])
            suggestions_edge.extend([
                "Stable sort when keys are equal",
                "Filter with special characters and unicode",
            ])
            suggestions_negative.extend([
                "Invalid sort key results in clear error or ignored parameter",
            ])

        if tokens & {"concurrent", "concurrency", "race", "parallel"}:
            suggestions_edge.extend([
                "Concurrent requests do not corrupt shared state",
                "Appropriate locking or transactional behavior under contention",
            ])
            suggestions_negative.extend([
                "Data inconsistency under concurrent writes is prevented",
            ])

        # Generic useful edge and security cases
        suggestions_edge.extend([
            "Very long input / large payloads",
            "Inputs with unicode and emoji",
            "Nulls and missing optional fields",
            "Fields with maximum allowed lengths",
        ])
        suggestions_security.extend([
            "SQL injection attempts are rejected",
            "Cross-site scripting payloads are sanitized",
            "Authorization checks prevent access to other users' data",
        ])

        # Deduplicate while preserving order
        def unique(seq):
            seen = set()
            out = []
            for s in seq:
                if s not in seen:
                    out.append(s)
                    seen.add(s)
            return out

        result["positive"] = unique(suggestions_positive)
        result["negative"] = unique(suggestions_negative)
        result["edge_cases"] = unique(suggestions_edge)
        result["security"] = unique(suggestions_security)

    return result

def analyze_requirement(description: str) -> dict:
    """
    Determine priority, risk_level, quality_score and recommended automation strategies
    from requirement description using keyword heuristics and a small scoring model.
    """
    description_lower = description.lower()

    # Base values
    priority = "MEDIUM"
    risk_level = "MEDIUM"
    quality_score = 65
    recommended_automation = ["API test with pytest/httpx"]

    # Keyword groups with weights for risk and priority adjustments
    high_impact_keywords = {"payment", "pay", "transaction", "checkout", "refund"}
    auth_keywords = {"login", "auth", "authentication", "password", "mfa", "oauth", "sso"}
    admin_keywords = {"admin", "administrator", "manage users", "privilege"}
    pii_keywords = {"ssn", "social security", "personal", "pii", "personal data", "email", "phone", "address"}
    security_keywords = {"security", "attack", "xss", "sql injection", "csrf", "vulnerability"}
    availability_keywords = {"uptime", "availability", "scale", "performance", "latency", "throughput"}
    regulatory_keywords = {"gdpr", "pci", "hipaa", "compliance", "regulation"}

    tokens = set(re.findall(r"\w+", description_lower))

    # Scoring adjustments
    score_modifier = 0
    risk_modifier = 0

    if tokens & high_impact_keywords:
        score_modifier += 20
        risk_modifier += 2
        recommended_automation.extend([
            "End-to-end flow test",
            "Transaction rollback test",
            "Integration test with payment gateway (mocked)",
        ])

    if tokens & auth_keywords:
        score_modifier += 10
        risk_modifier += 1
        recommended_automation.extend([
            "Authentication integration test",
            "UI automation for login flows (Playwright)",
            "MFA & session management tests",
        ])

    if tokens & admin_keywords:
        score_modifier += 10
        risk_modifier += 2
        recommended_automation.append("Authorization and RBAC tests")

    if tokens & pii_keywords:
        score_modifier += 15
        risk_modifier += 2
        recommended_automation.append("Data protection and masking tests")

    if tokens & security_keywords:
        score_modifier += 15
        risk_modifier += 2
        recommended_automation.append("Security regression test (SAST/DAST where applicable)")

    if tokens & availability_keywords:
        score_modifier += 5
        # availability increases operational risk but not necessarily data risk
        risk_modifier += 1
        recommended_automation.append("Performance and load tests")

    if tokens & regulatory_keywords:
        score_modifier += 20
        risk_modifier += 3
        recommended_automation.append("Compliance test cases and audit logs verification")

    # Adjust for unknown/short descriptions
    word_count = len(description.split())
    if word_count < 5:
        score_modifier -= 15

    # Estimate complexity from presence of integration words
    complexity_indicators = {"integration", "third-party", "gateway", "oauth", "sso", "email service", "sms"}
    if tokens & complexity_indicators:
        score_modifier += 10

    # Compute final quality score and risk_level / priority mapping
    quality_score = max(0, min(100, quality_score + score_modifier))

    # Derive risk_level from risk_modifier and keywords
    if risk_modifier >= 5 or (tokens & high_impact_keywords and tokens & regulatory_keywords):
        risk_level = "CRITICAL"
    elif risk_modifier >= 3:
        risk_level = "HIGH"
    elif risk_modifier == 2:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Derive priority: take into account risk and quality (lower quality => higher priority to improve tests)
    if risk_level == "CRITICAL":
        priority = "CRITICAL"
    elif risk_level == "HIGH":
        priority = "HIGH"
    else:
        # bump priority if quality is low
        if quality_score < 50:
            priority = "HIGH"
        elif quality_score < 70:
            priority = "MEDIUM"
        else:
            priority = "LOW"

    # Ensure recommended_automation is unique and ordered
    def unique(seq):
        seen = set()
        out = []
        for s in seq:
            if s not in seen:
                out.append(s)
                seen.add(s)
        return out

    recommended_automation = unique(recommended_automation)

    return {
        "priority": priority,
        "risk_level": risk_level,
        "quality_score": quality_score,
        "recommended_automation": recommended_automation,
    }