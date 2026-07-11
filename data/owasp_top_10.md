# OWASP Top 10 Security Vulnerabilities

1. **Broken Access Control**: Restrictions on what authenticated users are allowed to do are often not properly enforced. Attackers can exploit these flaws to access unauthorized functionality and/or data.
2. **Cryptographic Failures**: Failures related to cryptography (or lack thereof) which often lead to sensitive data exposure.
3. **Injection**: Injection flaws, such as SQL, NoSQL, OS, and LDAP injection, occur when untrusted data is sent to an interpreter as part of a command or query.
4. **Insecure Design**: Missing or ineffective control design.
5. **Security Misconfiguration**: Security controls are inaccurately configured or left insecure by default (e.g., open cloud storage, verbose error messages).
6. **Vulnerable and Outdated Components**: Components, such as libraries, frameworks, and other software modules, run with the same privileges as the application. If a vulnerable component is exploited, such an attack can facilitate serious data loss or server takeover.
7. **Identification and Authentication Failures**: Confirmation of the user's identity, authentication, and session management is not handled correctly.
8. **Software and Data Integrity Failures**: Code and infrastructure that does not protect against integrity violations (e.g., pulling plugins from untrusted sources).
9. **Security Logging and Monitoring Failures**: Without logging and monitoring, breaches cannot be detected.
10. **Server-Side Request Forgery (SSRF)**: SSRF flaws occur whenever a web application is fetching a remote resource without validating the user-supplied URL.
