# Security Advisory - Next.js Vulnerability Fix

## Date: 2026-02-05

## Severity: CRITICAL

## Summary

Fixed multiple critical security vulnerabilities in Next.js dependency by upgrading from version 16.0.1 to 16.1.5.

## Vulnerabilities Fixed

### 1. DoS (Denial of Service) Vulnerabilities
**CVE**: HTTP request deserialization can lead to DoS when using insecure React Server Components

**Affected Versions**: 
- >= 13.0.0, < 15.0.8
- >= 15.1.1-canary.0, < 15.1.12
- >= 15.2.0-canary.0, < 15.2.9
- >= 15.3.0-canary.0, < 15.3.9
- >= 15.4.0-canary.0, < 15.4.11
- >= 15.5.1-canary.0, < 15.5.10
- >= 15.6.0-canary.0, < 15.6.0-canary.61
- >= 16.0.0-beta.0, < 16.0.11
- >= 16.1.0-canary.0, < 16.1.5

**Impact**: Attackers could cause denial of service through malicious HTTP requests

### 2. RCE (Remote Code Execution) Vulnerabilities
**CVE**: Next.js is vulnerable to RCE in React flight protocol

**Affected Versions**:
- >= 14.3.0-canary.77, < 15.0.5
- >= 15.1.0-canary.0, < 15.1.9
- >= 15.2.0-canary.0, < 15.2.6
- >= 15.3.0-canary.0, < 15.3.6
- >= 15.4.0-canary.0, < 15.4.8
- >= 15.5.0-canary.0, < 15.5.7
- >= 16.0.0-canary.0, < 16.0.7

**Impact**: Attackers could potentially execute arbitrary code on the server

## Fix Applied

**Previous Version**: Next.js 16.0.1  
**Updated Version**: Next.js 16.1.5

**File Changed**: 
- `frontend/package.json`

## Action Required

If you have already cloned this repository with the old version, please:

1. Update your dependencies:
   ```bash
   cd ai_agents/agents/examples/bisheng-ai-integration/frontend
   npm install
   # or
   bun install
   ```

2. Verify the Next.js version:
   ```bash
   npm list next
   ```

3. Rebuild your application:
   ```bash
   npm run build
   ```

## Verification

After updating, verify that Next.js 16.1.5 or higher is installed:

```bash
cd frontend
npm list next
```

Expected output:
```
next@16.1.5
```

## References

- Next.js Security Advisories: https://github.com/vercel/next.js/security/advisories
- npm Advisory Database: https://github.com/advisories

## Recommendation

For production deployments:
1. Always use the latest stable version of Next.js
2. Enable automatic security updates in your CI/CD pipeline
3. Regularly check for security advisories
4. Use tools like `npm audit` or `bun audit` to detect vulnerabilities

## Contact

For security concerns, please report to the TEN framework security team.
