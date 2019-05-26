# Implementation notes

## 2019-04-09

There needs to be *TWO* annoy indices. Currently there is only one.
Therefore we need to:

  - Parameterize build_annoy_index
  - This is so that build_annoy_index can be generalize to two indices

annoy_index_collection suggested schema:

    {
      "annoy_index_name": string,
      "idx": integer
    }

When deleting annoy_index_collection entries, scope to only
select one particular annoy_index_name.

## 2019-04-05

### ScheduledJobs

Do the repetitive jobs:

  - Remodelling FastText
  - Rebuilding AnnoyIndex

### Subscriber

Subscriber will subscribe data from the downloaded_content

### API

Endpoints:

  - search
    - Search for entities
    -
  - details
  - top_people
