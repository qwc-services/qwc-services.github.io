+++
title = "Authentication"
date = 2021-09-17T16:40:01+02:00
weight = 6
chapter = true
+++

# Authentication services

There are multiple authentication backends: consult the navigation side-bar on the left.

## Troubleshooting: Login redirects to http instead of https

This happens, when the `X-Forwarded-Proto` header is not set to `https`. In that
case you need to force it in the nginx config:

```
location ~ /ldap-auth/ {
    proxy_set_header Host REPLACE_THIS.WITH.THE.HOSTNAME.OF.YOUR.SERVI.CE:PORTNUMBER;
    proxy_set_header X-Forwarded-Proto https;
    rewrite    ^/[^/]+(.+) $1 break;
    proxy_pass http://qwc-ldap-auth-service:9090;
}
```

It might be necessary to do the same to the `/qwc_admin` location configuration.
