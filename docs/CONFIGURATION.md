# Configuration Reference

`StaticSiteProps` defines the public configuration passed to the `StaticSite` construct. The
consuming CDK application remains responsible for reading context, environment variables, or
configuration files and converting them into these typed properties.

- [Properties](#properties)
- [Cache Semantics](#cache-semantics)
- [CloudFront-Only Domain](#cloudfront-only-domain)
- [Externally Managed DNS](#externally-managed-dns)
- [Route 53 and ACM](#route-53-and-acm)
- [Validation Rules](#validation-rules)
- [Security Policy Customization](#security-policy-customization)

## Properties

| Property | Default | Purpose |
| --- | --- | --- |
| `site_content_path` | `None` | Local directory deployed to the content bucket; omit to manage objects separately. |
| `domain_names` | `()` | CloudFront aliases, with the primary name first. |
| `certificate` | `None` | Existing ACM certificate for `domain_names`. |
| `hosted_zone` | `None` | Existing Route 53 public hosted zone used for optional certificate validation and aliases. |
| `create_certificate` | `False` | Create a DNS-validated ACM certificate using `hosted_zone`. |
| `create_route53_records` | `False` | Create A and AAAA CloudFront aliases for every configured domain. |
| `default_root_object` | `"index.html"` | Object CloudFront returns for the distribution root. |
| `error_document` | `"404.html"` | Object returned with HTTP 404 for S3 403 and 404 responses. |
| `static_asset_paths` | Common asset paths | CloudFront path patterns using optimized caching. |
| `immutable_asset_paths` | `()` | Opt-in deployment filters for content-addressed assets that receive optimized CloudFront caching and immutable browser metadata. |
| `content_security_policy` | Restrictive same-origin policy | Content Security Policy emitted through CloudFront. |
| `price_class` | `PRICE_CLASS_100` | CloudFront edge-location price class. |
| `enable_access_logs` | `False` | Create bounded S3 access-log storage and enable CloudFront standard logging. |
| `access_log_retention_days` | `30` | Number of days access logs remain in S3. |
| `bucket_removal_policy` | `RETAIN` | CloudFormation removal policy for the content bucket. |
| `versioned` | `True` | Enable S3 object versioning. |
| `deployment_cache_max_age_seconds` | `300` | Cache-Control maximum age applied to HTML and other mutable content. |
| `immutable_asset_cache_max_age_seconds` | `31536000` | Cache-Control maximum age applied to paths in `immutable_asset_paths`. |

## Cache Semantics

The optional content deployment assigns `public, max-age=300, must-revalidate` to HTML and other
mutable files. Paths explicitly listed in `immutable_asset_paths` are deployed separately with
`public, max-age=31536000, immutable`; they also receive an optimized CloudFront cache behavior.
Both deployments prune only the paths they manage and invalidate their corresponding CloudFront
paths.

Use the immutable policy only for content-addressed filenames, such as `build/app.a1b2c3.js`, whose
URL changes whenever its bytes change:

```python
StaticSiteProps(
    site_content_path='site',
    immutable_asset_paths=('build/*',),
)
```

Do not classify stable filenames such as `index.html`, `favicon.ico`, or `app.js` as immutable.
Browsers may reuse those objects for the full configured lifetime without checking for updates.

## CloudFront-Only Domain

Omit domain and certificate properties to use the generated CloudFront hostname:

```python
site = StaticSite(self, 'Site')
```

The hostname is available from
`site.distribution.distribution_domain_name`.

See the runnable [generated-hostname example](../examples/cloudfront-domain/app.py).

## Externally Managed DNS

Import an ACM certificate and configure only the names served by CloudFront:

```python
certificate = acm.Certificate.from_certificate_arn(
    self,
    'Certificate',
    certificate_arn,
)
site = StaticSite(
    self,
    'Site',
    props=StaticSiteProps(
        domain_names=('www.example.com',),
        certificate=certificate,
        site_content_path='site',
    ),
)
```

Create the required CNAME or equivalent record with the external DNS provider. The construct
deliberately does not modify external DNS.

See the runnable [external-DNS example](../examples/external-dns/app.py).

## Route 53 and ACM

To manage aliases and certificate validation in the consuming stack:

```python
site = StaticSite(
    self,
    'Site',
    props=StaticSiteProps(
        domain_names=('example.com', 'www.example.com'),
        hosted_zone=hosted_zone,
        create_certificate=True,
        create_route53_records=True,
        site_content_path='site',
    ),
)
```

CloudFront requires an ACM certificate in `us-east-1`. A stack using `create_certificate=True` must
therefore be deployed in `us-east-1`. Applications using another deployment region should provision
the certificate separately in `us-east-1` and pass it through `certificate`. The construct rejects
certificate creation when the stack region is unresolved or is not `us-east-1`.

See the runnable [Route 53 example](../examples/route53-managed/app.py).

## Validation Rules

Configuration fails before synthesis when it contains incomplete combinations,
including:

- Domain names without an existing or construct-created certificate;
- Both `certificate` and `create_certificate=True`;
- Certificate creation or Route 53 records without a hosted zone and domain names;
- Certificate creation in an environment-agnostic stack or a region other than `us-east-1`;
- Empty or duplicate domain and path patterns;
- Nonpositive log retention or immutable cache lifetime values; or
- Negative mutable-content cache lifetime values.

## Security Policy Customization

The default Content Security Policy allows same-origin scripts, styles, fonts, images, and
connections, plus `data:` images. A consuming site that uses external analytics, fonts, forms, or
media must supply an explicit policy that permits only the required origins. Test the resulting
headers in a representative environment before deploying production.

See the runnable [custom-CSP example](../examples/custom-csp/app.py). Additional focused examples
cover [access logging](../examples/access-logging/app.py) and
[externally managed content](../examples/external-content/app.py).
