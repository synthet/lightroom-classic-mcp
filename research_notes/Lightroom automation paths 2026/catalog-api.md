# Lightroom Catalog REST API

Research date: 2026-10-20. Scope is the cloud Lightroom Services / Catalog API documented at `developer.adobe.com/lightroom/lightroom-api-docs` and its source repo `AdobeDocs/lightroom-public-apis`. The Firefly Services Lightroom imaging API is mentioned only where an official page distinguishes it.

Primary spec used for the operation list: OpenAPI document `static/swagger.json` on `main` at commit `e6d8ae839f4163985c56a995c873d9176c370e3b` (2026-08-19). Raw file: https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json. A direct GET of https://developer.adobe.com/lightroom/lightroom-api-docs/swagger.json returned HTTP 404 on this date, so the live rendered reference could not be byte-compared with that file. The API reference page declares `data-src=/lightroom/lightroom-api-docs/swagger.json` — [API reference](https://developer.adobe.com/lightroom/lightroom-api-docs/api/).

## What is the official base URL, current documentation URL, and the latest published changelog or docs update date?

### Takeaway
The service base URL is `https://lr.adobe.io`, with `/v2/...` paths. The published changelog’s last versioned capability entry is still Version 1.2.1 (18 May 2021). The docs repository has later edits, including an OpenAPI addition of export operations on 19 August 2026 that the changelog page does not record.

### Cited Findings
- Overview title is “Adobe Lightroom API”; it says Photoshop Lightroom stores user assets, metadata, and media renditions “in a catalog in the cloud,” and points readers to Getting Started. The page has no visible last-updated date. — [Overview](https://developer.adobe.com/lightroom/lightroom-api-docs/)
- The same overview says documentation source is a GitHub repo and invites pull requests. The repo homepage is https://developer.adobe.com/lightroom/lightroom-api-docs/. — [Overview](https://developer.adobe.com/lightroom/lightroom-api-docs/); [AdobeDocs/lightroom-public-apis](https://github.com/AdobeDocs/lightroom-public-apis)
- Upload guide: “Use the base endpoint https://lr.adobe.io for all APIs.” Catalog lookup is `GET /v2/catalog`. A sample catalog object includes `"base": "<base_url>"`. — [Upload Customer Images and Videos](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/)
- Calling-API guide sample calls `https://lr.adobe.io/v2/...` with `X-API-Key` and `Authorization: Bearer`. — [Calling a Lightroom API](https://developer.adobe.com/lightroom/lightroom-api-docs/guides/calling-api/)
- OpenAPI `servers` is `[{"url": "https://lr.adobe.io/"}]`. `info.title` is “Lightroom API Documentation”. `info.version` is `1.0.0`. `openapi` is `3.0.1`. Description links the changelog at the release-notes URL below. The spec file itself has no changelog date. — [static/swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Links guide example uses a per-catalog base `https://lr.adobe.io/v2/catalogs/18c23e15/` plus relative `links`, and tells clients to resolve those with RFC 3986 rather than hard-coding URLs. — [Links and Pagination](https://developer.adobe.com/lightroom/lightroom-api-docs/guides/links-and-pagination/)
- Common data model example base is `https://lr.adobe.io/v2/catalogs/9479135e/`. — [Common Data Model](https://developer.adobe.com/lightroom/lightroom-api-docs/guides/common-data-model/)
- Current documentation index URLs (no page-level “last updated” date on the pages fetched): overview https://developer.adobe.com/lightroom/lightroom-api-docs/ ; getting started https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/ ; API reference https://developer.adobe.com/lightroom/lightroom-api-docs/api/ ; changelog https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/ ; authentication https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/authenticate-customers/ ; create integration https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/create-integration/.
- Published changelog page title is “API Change Logs”. Its newest section is “Version 1.2.1 (18 May, 2021)”. Older sections are “Version 1.2.0 (24 Feb, 2021)” and “Version 1.1.0 (3 Feb, 2021)”. The fetched page has no newer version heading and no separate page-updated timestamp. — [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/)
- Docs-repo commit history (not the changelog page), newest content commit when listed on 2026-10-20: 2026-08-19 `e6d8ae8` “Reapply ‘Adding export APIs that deal with c2pa signing to public docs (#81)’ (#82) (#83)”, +400 lines in `static/swagger.json` only. Immediately before that: 2026-07-30 revert `e0c1aa9`, and 2026-07-29 add `20cface` with the same message. — [Commits](https://github.com/AdobeDocs/lightroom-public-apis/commits/main); [e6d8ae8](https://github.com/AdobeDocs/lightroom-public-apis/commit/e6d8ae8)
- Other 2026 docs-repo commits, distinct from the changelog page: 2026-06-24 `9eb38ed` documents string `code` 403s on `GET /v2/catalog` and states the PR is documentation-only; 2026-05-28 `bcc39dd` “[update-bot] Content update”; 2026-04-25 `3f9c079` “Add HTTP 429 rate limit documentation”; 2026-04-06 `5ea96a8` “Eds migration”; 2026-04-01 `37f3341` “Adding Content Credentials to the fullsize rendition info”. — [Commits](https://github.com/AdobeDocs/lightroom-public-apis/commits/main); [PR 79](https://github.com/AdobeDocs/lightroom-public-apis/pull/79); [PR 77](https://github.com/AdobeDocs/lightroom-public-apis/pull/77)
- OpenAPI `info.version` `1.0.0` does not match changelog labels 1.1.0 / 1.2.0 / 1.2.1. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json); [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/)

### Inferences
- Treat 18 May 2021 as the last date Adobe published on the changelog page. Treat 19 August 2026 as the newest dated change to the OpenAPI file in the official docs repo. Those are different events: the August 2026 commit adds export operations to the spec; the changelog page was not updated to match.
- The 2026-06-24 and 2026-04-25 commits are documentation of existing error behavior (string 403 codes; HTTP 429 after a “CGW migration”), not new resource paths. The 2026-05-28 bot commit was not opened, so it is not classified.

### Gaps
- No “last updated” timestamp was present on the HTML pages fetched from developer.adobe.com.
- https://developer.adobe.com/lightroom/lightroom-api-docs/swagger.json returned 404, so it is unverified whether production has deployed commit `e6d8ae8`.
- Contents of the 2026-05-28 `[update-bot] Content update` commit were not read.

## How does a developer get access, and which OAuth scopes are required?

### Takeaway
Adobe documents both a self-serve Adobe I/O Console path (“Lightroom Services” under Creative Cloud) and partner-entitlement language. Tokens must include `openid`, `AdobeID`, `lr_partner_apis`, and `lr_partner_rendition_apis`. Refresh-token renewal, and on-demand `fullsize` / `2560` renditions, are documented as extra capabilities that require contacting Adobe.

### Cited Findings
- Getting Started: “These APIs are available only to entitled partner applications that have authenticated the customer, and the customer has given their express permission to the client to act on their behalf.” Partners “must register a new integration with Adobe” for an API key, then use Adobe IMS OAuth 2.0. The access token and API key go on privileged requests. — [Getting Started](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/)
- Create Integration walkthrough: (1) Adobe ID to administer the integration; (2) log into the “Adobe I/O Console”, “Create new project”, “Add API”; (3) under “Creative Cloud”, select “Lightroom Services” and “Continue”, then complete the OAuth integration form for an API key and client secret; (4) verify with a health check and by authenticating customers. It points at “Adobe I/O OAuth Integration documentation” but the fetched page does not include that URL. — [Creating an Integration](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/create-integration/)
- Authentication page: “Registered partner applications are entitled to access Lightroom customer content” with an IMS user access token. “Partner applications must include the `lr_partner_apis` and `lr_partner_rendition_apis` scope (along with the standard `openid` and `AdobeID` scopes) to access the Lightroom Services.” Refresh-token renewal: “additional setup is needed on the API key. Should your application require this capability, you must contact Adobe and describe your needs.” Sample instructions say to replace a `creative_sdk` scope with `lr_partner_apis,lr_partner_rendition_apis`. — [Authenticating Customers](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/authenticate-customers/)
- OpenAPI header `X-API-Key` description, repeated on operations: “Client ID (API Key) which is subscribed to the Lightroom APIs through console.adobe.io”. `Authorization` is “Bearer [token] - User access token of an authenticated Lightroom customer”. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Every call needs `X-API-Key` and `Authorization: Bearer`. Applications “must acquire an API key by registering an integration as an Adobe partner.” — [Calling a Lightroom API](https://developer.adobe.com/lightroom/lightroom-api-docs/guides/calling-api/)
- Customer precondition: `GET /v2/account`. `entitlement.status` must be `subscriber` or `trial`, or other Lightroom calls return `403 Forbidden`. Also check `entitlement.storage.used` against `entitlement.storage.limit`. — [Upload Customer Images and Videos](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/)
- `GET /v2/catalog` “will fail with a `403` if the user has no catalog and a new catalog cannot be generated; otherwise it will return the catalog information.” The same page also says that if the user has no catalog, the app can tell them they must first log into an Adobe Lightroom client before upload. — [Upload Customer Images and Videos](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/)
- `fullsize` and `2560` renditions “are not available with basic API access. Should your application require this capability, you must contact Adobe and describe your needs.” — [Read and Generate Renditions](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/read-generate-renditions/)
- Official samples README (docs repo): create an integration with `Lightroom Services` for an API key and client secret, then an OAuth 2.0 user access token “with the `openid`, `lr_partner_apis` and `lr_partner_rendition_apis` scopes.” `LrSession` checks account status `trial` or `subscriber` and that a catalog exists. — [samples README](https://github.com/AdobeDocs/lightroom-public-apis/tree/main/samples)
- `lr_partner_rendition_apis` was added to the docs repo on 2022-01-20, commit message “Adding information about lr_partner_rendition_apis scope (#22)”. — [Commits](https://github.com/AdobeDocs/lightroom-public-apis/commits/main)

### Inferences
- Access is both: the published steps are a self-serve Console project that adds “Lightroom Services”, and the prose still calls the caller an entitled / registered partner. Nothing on the pages opened describes a separate partner-application form in front of that Console click-path. Extra gates that do say “contact Adobe” are refresh-token renewal and basic-vs-fullsize/2560 rendition access.
- `lr_partner_rendition_apis` is documented as required to access Lightroom Services at all, alongside `lr_partner_apis`, not only for the rendition calls. The pages opened do not define a split where one scope is catalog-only and the other is rendition-only.

### Gaps
- The Adobe I/O OAuth Integration document linked from Creating an Integration was not opened (URL not present in the fetched page).
- Whether “Lightroom Services” is visible to every Console user, or only after an Adobe-side entitlement, is not stated. The pages do not say “partner-only, no Console” and do not say “every Adobe ID can call the API without review.”
- A 2022 community thread about `invalid_scope` for `lr_partner_rendition_apis` was not used as evidence. It is secondary and was not needed to locate the official scope page.

## What catalog, album, asset, upload, rendition, and metadata operations are documented?

### Takeaway
The OpenAPI file documents 20 operations under five tags (Health, Accounts, Catalogs, Assets, Albums). There is no separate metadata-write resource. Asset “metadata” on create is capture date plus import source. Album metadata is the album payload, including partner `publishInfo`. A `develop` object appears in the asset response example; it is not a field on the create-asset request schema.

### Cited Findings
- Tags and descriptions: Health “Lightroom Services status.” Accounts “Account information for the authenticated user.” Catalogs “Catalog information for the authenticated user.” Assets “Information for assets, typically images or videos.” Albums “Information for albums, which contain references to zero or more assets.” — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Operations present in that file (method, path, `operationId`, summary):
  - `GET /v2/health` — `getHealth` — “Lightroom Services health check”. Returns a server version ID “if the services are up.”
  - `GET /v2/account` — `getAccount` — “Retrieve the user account metadata”.
  - `GET /v2/catalog` — `getCatalog` — “Retrieve the user catalog metadata”. “A catalog is the topmost container of resources for a user.”
  - `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}` — `createAsset` — “Create asset”. “Create a new asset with initial metadata and import information.”
  - `GET /v2/catalogs/{catalog_id}/assets/{asset_id}` — `getAsset` — “Get a catalog asset”.
  - `GET /v2/catalogs/{catalog_id}/assets` — `getAssets` — “Retrieve assets”.
  - `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}/master` — `createAssetOriginal` — “Create an asset original file”. Up to 200 MB per call; larger files use repeated calls with `Content-Range`.
  - `POST /v2/catalogs/{catalog_id}/assets/{asset_id}/renditions` — `generateRenditions` — “Generate renditions for an original file”. Header `X-Generate-Renditions`: “Supported rendition types are : ['fullsize', '2560'].” No request body. “Generated rendition will be deleted after 1 day automatically.”
  - `GET /v2/catalogs/{catalog_id}/assets/{asset_id}/renditions/{rendition_type}` — `getAssetRendition` — “Get latest asset rendition”. Path description: “Supported rendition types are : ['thumbnail2x', 'fullsize', '640', '1280', '2048', '2560'].”
  - `POST /v2/catalogs/{catalog_id}/assets/{asset_id}/exports` — `generateExport` — “Generate a signed export for an asset”. “optionally embedding a signed C2PA Content Credentials manifest. Allowed output sizes are 2048, 4096 and fullsize. Only JPEG output is supported.”
  - `GET /v2/catalogs/{catalog_id}/assets/{asset_id}/exports/{export_id}` — `getAssetExport` — “Get a generated export”.
  - `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}/xmp/develop` — `putAssetExternalXmpDevelopSetting` — “Create asset external xmp develop setting file”.
  - `GET /v2/catalogs/{catalog_id}/assets/{asset_id}/xmp/develop` — `getAssetExternalXmpDevelopSetting` — “Get latest asset external xmp develop setting”.
  - `PUT /v2/catalogs/{catalog_id}/albums/{album_id}` — `createAlbum` — “Create album”.
  - `GET /v2/catalogs/{catalog_id}/albums/{album_id}` — `readAlbum` — “Get album”.
  - `POST /v2/catalogs/{catalog_id}/albums/{album_id}` — `updateAlbum` — “Update album”. “The existing album should be created via the same client app and of subtype project or project_set.”
  - `DELETE /v2/catalogs/{catalog_id}/albums/{album_id}` — `deleteAlbum` — “Delete album”. Same same-client and `project` or `project_set` constraint.
  - `GET /v2/catalogs/{catalog_id}/albums` — `getAlbums` — “Retrieve albums”.
  - `PUT /v2/catalogs/{catalog_id}/albums/{album_id}/assets` — `addAssetsToAlbum` — “Add assets to album”.
  - `GET /v2/catalogs/{catalog_id}/albums/{album_id}/assets` — `listAssetsOfAlbum` — “List assets of an album”.
  — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Upload narrative (same paths): `GET /v2/health`, `GET /v2/account`, `GET /v2/catalog`, then `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}` with `subtype`, `payload.captureDate`, and `payload.importSource` (`fileName`, `importedOnDevice`, `importedBy`, `importTimestamp`). Asset ids are RFC-4122 GUIDs without hyphens. Then `PUT .../master`. Max 200 MB per invocation. — [Upload Customer Images and Videos](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/)
- `createAsset` JSON body `required` is `captureDate`. Documented properties: `subtype` enum `image` | `video`; `payload.userCreated`; `payload.userUpdated`; `payload.captureDate` (ISO-8601, or `0000-00-00T00:00:00` to let the server fill it from the master); `payload.importSource.fileName`, `importedOnDevice`, `importedBy`, `importTimestamp`. The create schema does not list `develop`, keywords, rating, caption, or title. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- `SuccessImageAssetExample` payload keys are `captureDate`, `importSource` (adds `fileSize`, `originalWidth`, `originalHeight`, `sha256` on the example), a placeholder `"<key>": "<value>"`, and `develop: { "<dev_key>": "<dev_value>" }`. Links on that example: `self`, `/rels/master_create`, `/rels/xmp_develop_create`, `/rels/rendition_type/<rendition_type>`, `/rels/xmp/develop`. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- `GET` asset/list descriptions: a rendition link can be flagged invalid after an edit; new renditions “only 2560 and fullsize” can be generated. The read `xmp/develop` link is invalid if the asset was created with SHA256 but external xmp/develop has not been uploaded yet. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Rendition guide: on upload, JPEGs `thumbnail2x` (320 px on an edge), `640`, `1280`, and `2048` (long edge) are created. “Upon editing a photo,” those same four are recreated “with all edits applied.” `fullsize` is “size of original with edits, constrained by any applied crops.” `2560` is 2560 px on the long edge. Both must be requested on demand, polled, and “will be deleted after 1 day.” The guide also documents `HEAD /v2/catalogs/{catalog_id}/assets/{asset_id}/renditions/<rendition_type>` as the poll. That HEAD method is not an operation in the OpenAPI path list above. Generate call returns HTTP 202 in the guide. — [Read and Generate Renditions](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/read-generate-renditions/)
- Export body requires `output_settings.long_side` enum `"2048"` | `"4096"` | `"fullsize"`. Optional `mime_type` enum `image/jpeg`. Optional `gain_map` boolean, “Whether to embed an HDR gain map in the exported JPEG, if available.” Optional `c2pa_settings`: `include` items `edit_list`, `producer`, `connected_accounts`; `storage_method` enum `embed`, `cloud`, `embed_and_cloud`. Example uses `include: ["edit_list", "producer"]` and `storage_method: "embed"`. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Album management: subtype `project` (and update/delete also allow `project_set`). `serviceId` must be the partner API key. `payload.name` is the user-visible name shown in Lightroom clients. `publishInfo` holds external affiliation (`version` 3, `remoteId`, `remoteLinks.edit` / `.view`, `servicePayload` max 1024 characters, optional `deleted` tombstone). Add assets with `PUT .../albums/{album_id}/assets`, up to 50 assets per call, optional `cover`, lex64 `order`, and per-asset `publishInfo`. Lightroom clients show recognized partners’ project albums in the Connections panel. Enumerate with `GET /v2/catalogs/{catalog_id}/albums?subtype=project`. — [Manage Content](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/manage-content/)
- `GET /v2/catalog` sample `links` include `/rels/collections` → `catalogs/<catalog_id>/albums?subtype=collection`, `/rels/images_videos`, `/rels/deleted_images_videos`, `/rels/catalog_spaces` → `catalogs/<catalog_id>/spaces?subtype=shared`, `/rels/updates`, `/rels/tasks/index`, `/rels/tasks/tag`. — [Upload Customer Images and Videos](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/)
- Those `spaces`, `updates`, and `tasks` hrefs do not appear as paths in the OpenAPI `paths` object. The only album subtype called out as a query in the manage-content guide is `project`. `collection` appears as a link query in the catalog sample, not as its own operation. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json); [Upload Customer Images and Videos](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/)
- Common model: top-level `base`, `id`, `created`, `updated`, `type`, `subtype` are server-constructed and “can not be modified by clients,” except subtype is “Provided by the client on creation.” `payload` is “Metadata about the object provided by the client.” — [Common Data Model](https://developer.adobe.com/lightroom/lightroom-api-docs/guides/common-data-model/)
- JSON responses are prepended with `while(1){}`, which clients must strip. Binary bodies are `application/octet-stream`. External XMP develop settings are `application/rdf+xml`. — [Calling a Lightroom API](https://developer.adobe.com/lightroom/lightroom-api-docs/guides/calling-api/)
- String search of the OpenAPI file: `keyword` 0, `mask` 0, `slider` 0, `lrcat` 0, `Firefly` 0, `deprecat` 0. `rating` occurs only as sort-enum values `ratingAsc` and `ratingDesc`. `metadata` occurs as the words “account metadata”, “catalog metadata”, “initial metadata”, and album/service payload descriptions, not as a metadata-field API. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)

### Inferences
- Catalog operations that are actually specified are get-account, get-catalog, and health. There is no documented create/update/delete catalog call. Album CRUD is limited, on update and delete, to albums that this client created and that are `project` or `project_set`.
- “Metadata” in this API means the JSON payload on create-asset and on albums, plus the XMP develop document. It does not mean a general EXIF/IPTC field writer. The `<dev_key>` object in the asset example is not, by itself, a documented slider or develop-settings write API.

### Gaps
- No operation was found for keywords, ratings, captions, titles, pick flags, GPS, or partial metadata update of an existing asset. Absence is from the OpenAPI path list and a string search, not from a limitations page that lists those fields.
- Behavior of the catalog-sample links for `spaces`, `updates`, `tasks`, and `subtype=collection` is not specified as operations in `swagger.json`. Not found as documented operations.
- `HEAD` on a rendition is in the renditions guide and not in the OpenAPI path map. Whether the service accepts HEAD is not confirmed beyond that guide.

## External develop XMP: which methods and paths exist, and is there a copy-from-asset operation?

### Takeaway
There is one path, `/v2/catalogs/{catalog_id}/assets/{asset_id}/xmp/develop`. `GET` reads the latest external XMP develop file (`application/rdf+xml`). `PUT` is documented as two workflows on that same operation: upload an RDF/XML body, or copy another asset’s external XMP by posting JSON `file_href`. There is no second path whose name is “copy develop settings.”

### Cited Findings
- Changelog Version 1.1.0 (3 Feb, 2021): “Added new Create External Develop XMP API (PUT)- `/v2/catalogs/{catalog_id}/assets/{asset_id}/xmp/develop`. It can be used to upload external xmp develop file for an asset.” “Added new Read External Develop XMP API (GET)- `/v2/catalogs/{catalog_id}/assets/{asset_id}/xmp/develop`. It can be used to get latest external xmp develop file for an asset.” That entry does not mention a copy-from-asset workflow. — [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/)
- Version 1.2.1 (18 May, 2021) added “Create xmp Develop Links” on `GET` asset, `GET` assets, and list-album-assets. It does not add a new XMP path. — [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/)
- Current operation, quoted from the OpenAPI description: `operationId` `putAssetExternalXmpDevelopSetting`. Summary: “Create asset external xmp develop setting file”. Description: “This API support two workflows. The first workflow is to upload external XMP develop settings file for the asset. Content-type header for this case is application/rdf+xml. The second workflow is to create an external XMP develop settings file by copying from another asset's external xmp develop setting file. Content-type header for this case is application/json.” — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Same operation, `Content-Type` parameter description: “For uploading a new xmp/develop file content-type='application/rdf+xml' and for copying xmp/develop file from another asset content-type='application/json'”. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Request body description: “The below request body example is for copying external xmp/develop file from another asset. (For upload external xmp/develop case the body will be a xml string. Eg. '\<xml.../xml\>')”. The only schema under `content` is `application/json`, property `file_href` (string): “External xmp/develop link of source asset.” Example: `"file_href": "/v2/catalogs/{catalog_id}/assets/{source_asset_id}/xmp/develop"`. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- `PUT` responses listed: 201 “Created”, plus 400, 401, 403, 404, 415, 503. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Read operation: `operationId` `getAssetExternalXmpDevelopSetting`. Summary: “Get latest asset external xmp develop setting”. Description: “Get latest asset external xmp develop setting file”. HTTP 200 description: “External XMP Develop Setting file. Content type of the response is application/rdf+xml.” The 200 response object has no schema and no `content` map. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- Calling-API guide: content type is JSON except binary (`application/octet-stream`) and “those that handle external XMP Develop Settings (content type application/rdf+xml).” It does not mention the JSON copy content type. — [Calling a Lightroom API](https://developer.adobe.com/lightroom/lightroom-api-docs/guides/calling-api/)
- No other path in the OpenAPI file contains `xmp` or an operationId containing copy. The word “copy” appears in the PUT description, the Content-Type parameter, and the request-body description (three hits). — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)

### Inferences
- A copy-from-asset behavior is documented, but only as the `application/json` mode of `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}/xmp/develop` (`putAssetExternalXmpDevelopSetting`), with `file_href` pointing at the source asset’s `/xmp/develop` link. It is not a separate method or path.
- The RDF upload body is described in prose. The OpenAPI `requestBody.content` object does not declare `application/rdf+xml`, so a codegen client that trusts only the content map would see the JSON copy body and not the XML upload.
- The 2021 changelog text is narrower than the current spec: upload and read only. The date the JSON copy wording was added was not established.

### Gaps
- Not found: an operation whose name or path is specifically “copy develop settings from asset A to asset B” other than the JSON `file_href` mode above.
- Not found: a schema for the RDF/XML develop document (which `crs:` fields, masks, or AI edits are accepted).
- Not found: a commit date for when the two-workflow / `file_href` text first appeared. It is present in `main` as of commit `e6d8ae8` (2026-08-19) and was not part of the 3 Feb 2021 changelog wording.

## What the docs say this API cannot do

### Takeaway
The docs do not contain a limitations section that names desktop UI, local `.lrcat` files, interactive sliders, or “newer AI edits” as unsupported. What they do state is that this is a cloud-catalog REST API, that Lightroom Classic is a separate extensibility surface, that fullsize/2560 renditions need extra approval, and that generative-AI pixels delivered outside Adobe need Content Credentials, which this print-rendition workflow supports only on `fullsize`.

### Cited Findings
- Product framing: assets, metadata, and renditions live “in a catalog in the cloud.” — [Overview](https://developer.adobe.com/lightroom/lightroom-api-docs/); [Getting Started](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/)
- Creative Cloud platform page lists two different entries. “Lightroom Services”: “Streamline photography workflows for customers with content in Lightroom, through RESTful APIs.” “Lightroom Classic”: “Create effects, define presets and brushes, manipulate metadata, and much more in Lightroom.” — [Creative Cloud Developer Platform](https://developer.adobe.com/creative-cloud)
- The only `Classic` string in the OpenAPI file is the example catalog payload name “Lightroom Classic Catalog Name”, inside a presets/favorites example. It is not a statement about the desktop app. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- String search of that OpenAPI file: `lrcat` 0, `slider` 0, `mask` 0, `Firefly` 0, `keyword` 0. No path for a local catalog, a module, a view, or a slider. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- FAQ page body is the heading “All questions resolved” and the text “Lorem ipsum”. It does not list limitations. — [FAQ source](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/src/pages/support/FAQ/index.md) (published URL https://developer.adobe.com/lightroom/lightroom-api-docs/support/FAQ/)
- Developer guidelines: “Undocumented features and functionality may cease to work without notice in a future release.” “Please discuss any additional API or data needs with Adobe.” Abuse can lead to “revocation of your license keys.” This is a warning about undocumented behavior, not a feature blacklist. — [Developer Guidelines](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/developer-guidelines/)
- `fullsize` and `2560` “are not available with basic API access.” — [Read and Generate Renditions](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/read-generate-renditions/)
- Same renditions page, on generative AI: “Images that include generative AI (Gen AI) require Content Credentials (C2PA) when they are delivered outside Adobe's services, so recipients get accurate Gen AI disclosure embedded in the file. In this print renditions workflow, that Content Credentials / Gen AI treatment is available only for fullsize renditions. Other rendition sizes or types i.e 2560 are not supported.” — [Read and Generate Renditions](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/read-generate-renditions/)
- Top-level catalog/asset envelope fields “can not be modified by clients” (the common data model’s wording). Payload is the client-writable part, and “Values supported within the payload generally differ for each document type.” — [Common Data Model](https://developer.adobe.com/lightroom/lightroom-api-docs/guides/common-data-model/)
- Update and delete album: only an album “created via the same client app and of subtype project or project_set.” — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json); also [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/) Version 1.1.0
- Upload is for users who already have a Lightroom account “with an active subscription and an existing catalog” with enough storage. Entitlement other than `subscriber` or `trial` leads to 403 on other calls. — [Upload Customer Images and Videos](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/)

### Inferences
- Desktop Lightroom Classic UI automation, a local `.lrcat`, and interactive develop sliders are outside the documented surface because the documented surface is cloud REST resources (catalog, asset, album, master bytes, renditions, exports, XMP document) and the platform page treats Lightroom Classic as a different extensibility product. That is an inference from what is specified, not a quoted “cannot.”
- The Gen AI sentence constrains Content Credentials on outbound fullsize renditions. It does not say the Catalog API can or cannot apply newer AI edits.

### Gaps
- Not found, on the pages opened, an official sentence that this Catalog API cannot drive the desktop UI, open a `.lrcat`, move interactive sliders, or apply newer AI edits (masks, adaptive presets, Denoise, and similar). Pages checked for that wording: overview, getting started, create-integration, authenticate-customers, developer-guidelines, upload-content, manage-content, read-generate-renditions, calling-api, links-and-pagination, common-data-model, release-notes, API reference shell, FAQ source, Creative Cloud platform page, and `static/swagger.json`.

## Any 2025-2026 deprecation, entitlement, or breaking-change notice for this catalog API, as distinct from Firefly?

### Takeaway
The Catalog API changelog has no 2025 or 2026 entry. Its last deprecation wording is from February 2021 and is about revision-scoped create/upload paths. 2026 changes in the docs repo are an export/C2PA spec addition, plus documentation of 403 entitlement errors and HTTP 429. A “Lightroom API” end-of-life date of 31 July 2026 is published on the Firefly Services Lightroom page, which is a different doc set and was not found on the Catalog API changelog.

### Cited Findings
- Catalog changelog sections stop at Version 1.2.1 (18 May, 2021). No 2025 or 2026 heading is on that page. — [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/)
- February 2021 deprecations, still the only “deprecated” wording on that page: Version 1.2.0 (24 Feb, 2021) says `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}/revisions/{revision_id}/master` “is removed and will be deprecated soon”; use `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}/master`. Version 1.1.0 (3 Feb, 2021) says `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}/revisions/{revision_id}` “is removed and will be deprecated soon”; use `PUT /v2/catalogs/{catalog_id}/assets/{asset_id}`. — [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/)
- OpenAPI file contains zero matches for “deprecat”. — [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- 2026-06-24, docs repo, commit `9eb38ed` / PR 79: adds `UnexpectedEntitlementError` and `EntitlementExpiredError` to `GET /v2/catalog` 403 responses. PR text: “this PR is documentation-only.” It says a third-party caller received `code` as the string `"UnexpectedEntitlementError"` for an account that was not an active subscriber, and that string codes “have been allowed to be strings as well as integers for a long time.” Schema description: “Returned when the resource owner's account is in an unexpected entitlement state for the requested operation (for example, a partner request on behalf of an account that is not an active subscriber).” `description` enum: “Account is in an unexpected status”. `errors.catalog` enum: “not allowed”. `EntitlementExpiredError` description enum: “Resources unavailable because owner account entitlement has expired”. Related integer form still in the spec: `AccessForbiddenAccountStateError` code `4301`, description “Access forbidden due to account state of resource owner”. — [PR 79](https://github.com/AdobeDocs/lightroom-public-apis/pull/79); [commit 9eb38ed](https://github.com/AdobeDocs/lightroom-public-apis/commit/9eb38ed04ccbb1e0494995fdc5558c4ef105fe6e); [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)
- 2026-04-25, PR 77: “Document the HTTP 429 (Too Many Requests) error response behavior after CGW migration.” “429 responses have empty bodies and should be handled with exponential backoff retry.” The PR checklist item is “Documentation update for Lightroom public Apis.” The upload guide and developer guidelines now say HTTP 429 has an empty body and should be retried with exponential backoff; developer guidelines cap retries at 3. — [PR 77](https://github.com/AdobeDocs/lightroom-public-apis/pull/77); [Upload Customer Images and Videos](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/); [Developer Guidelines](https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/developer-guidelines/)
- 2026-07-29 through 2026-08-19: export operations `generateExport` and `getAssetExport` were added to the public OpenAPI, reverted the next day, then reapplied on 2026-08-19. That is a spec addition of C2PA-signed JPEG export. It is not listed on the changelog page. — [e6d8ae8](https://github.com/AdobeDocs/lightroom-public-apis/commit/e6d8ae8); [Commits](https://github.com/AdobeDocs/lightroom-public-apis/commits/main); [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/)
- Firefly Services page, title “Adobe Lightroom API - Firefly Services”: “Lightroom API End-of-Life Notice. The Lightroom API will reach end-of-life on July 31, 2026.” Overview sentence: “Welcome to the Adobe Lightroom API, now integrated into Firefly Services.” The fetched page does not mention `lr.adobe.io` or the Catalog API paths. — [Firefly Services Lightroom overview](https://developer.adobe.com/firefly-services/docs/lightroom/)
- A Firefly Services quickstart uses host `https://image.adobe.io/lrService/autoStraighten` and tells the reader to get “a Lightroom or a Firefly Services Client ID” from the Adobe Developer Console. That page was not used to inventory imaging operations. — [Lightroom API Quickstart](https://developer.adobe.com/firefly-services/docs/lightroom/guides/quickstart/)
- The Catalog API changelog, overview, and OpenAPI file, as fetched, do not contain the sentence “end-of-life on July 31, 2026.” — [API Change Logs](https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/); [Overview](https://developer.adobe.com/lightroom/lightroom-api-docs/); [swagger.json](https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json)

### Inferences
- The 31 July 2026 end-of-life notice belongs to the Firefly Services document titled “Adobe Lightroom API - Firefly Services,” not to the changelog of the `lr.adobe.io` Catalog API. The two docs were both live on 2026-10-20, which is after that date, and they were not cross-linked in the pages fetched.
- For the Catalog API, the 2026 entitlement text is a documentation of 403s (`UnexpectedEntitlementError`, `EntitlementExpiredError`, and integer `4301`), which the AdobeDocs PR says were already the service’s behavior. It is not written as a new 2026 cutoff.
- HTTP 429 documentation is tied to a “CGW migration” in the PR, but the PR classifies the change as documentation. No replacement base URL or removed Catalog endpoint is stated there.

### Gaps
- Not found: a Catalog API page that says the Firefly end-of-life does not apply to `lr.adobe.io`, or that the products are formally separate. The separation used here is which official site carries which statement.
- Not found: a 2025-2026 breaking-change or deprecation notice inside https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/.
- Secondary conflict, not used as fact: https://apis.io/apis/adobe-creative-cloud/lightroom-api/ describes base URL `https://lr.adobe.io` and also says “Part of Adobe Firefly Services.” That sentence is an aggregator claim and disagrees with the split between the two Adobe doc sites above.
- The 2026-04-01 “Content Credentials to the fullsize rendition info” commit diff was not read line by line. The current renditions guide text quoted in the previous section is the `main` copy of that topic.
- The 2026-05-28 update-bot commit was not inspected.

### Pages opened

Official Adobe pages and the official docs repo:

- https://developer.adobe.com/lightroom/lightroom-api-docs/
- https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/
- https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/create-integration/
- https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/authenticate-customers/
- https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/developer-guidelines/
- https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/upload-content/
- https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/manage-content/ (via raw GitHub source of the same page)
- https://developer.adobe.com/lightroom/lightroom-api-docs/getting-started/read-generate-renditions/ (via raw GitHub source)
- https://developer.adobe.com/lightroom/lightroom-api-docs/guides/calling-api/
- https://developer.adobe.com/lightroom/lightroom-api-docs/guides/links-and-pagination/
- https://developer.adobe.com/lightroom/lightroom-api-docs/guides/common-data-model/ (via raw GitHub source)
- https://developer.adobe.com/lightroom/lightroom-api-docs/release-notes/
- https://developer.adobe.com/lightroom/lightroom-api-docs/api/
- https://developer.adobe.com/lightroom/lightroom-api-docs/swagger.json (404)
- https://developer.adobe.com/lightroom/lightroom-api-docs/support/FAQ/ (via raw GitHub source; body is placeholder text)
- https://developer.adobe.com/creative-cloud
- https://developer.adobe.com/firefly-services/docs/lightroom/ (EOL notice only; imaging operations not inventoried)
- https://developer.adobe.com/firefly-services/docs/lightroom/guides/quickstart/ (host distinction only, from search extract)
- https://github.com/AdobeDocs/lightroom-public-apis
- https://github.com/AdobeDocs/lightroom-public-apis/commits/main
- https://raw.githubusercontent.com/AdobeDocs/lightroom-public-apis/main/static/swagger.json
- https://github.com/AdobeDocs/lightroom-public-apis/commit/e6d8ae8
- https://github.com/AdobeDocs/lightroom-public-apis/commit/9eb38ed04ccbb1e0494995fdc5558c4ef105fe6e
- https://github.com/AdobeDocs/lightroom-public-apis/pull/79
- https://github.com/AdobeDocs/lightroom-public-apis/pull/77
- https://github.com/AdobeDocs/lightroom-public-apis/tree/main/samples
