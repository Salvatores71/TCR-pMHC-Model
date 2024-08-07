import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
} from "@apollo/client/core";
import gql from "graphql-tag";

const httpLink = createHttpLink({
  uri: "https://data.rcsb.org/graphql",
});

// Cache implementation
const cache = new InMemoryCache();

// Create Apollo Client
const client = new ApolloClient({
  link: httpLink, // RCSB PDB GraphQL API URL
  cache,
});

// Define GraphQL Query
const GET_ENTRY_DETAILS = gql`
  query getEntryDetails($id: String!) {
    entries(entry_ids: [$id]) {
      rcsb_id
      struct {
        title
      }
      rcsb_accession_info {
        initial_release_date
      }
      audit_author {
        name
      }
      struct {
        title
      }
      struct_keywords {
        pdbx_keywords
        text
      }
      rcsb_accession_info {
        deposit_date
        initial_release_date
        major_revision
        minor_revision
      }
      pdbx_audit_support {
        funding_organization
        country
        grant_number
        ordinal
      }
    }
  }
`;

// Fetch Entry Details Function
export async function fetchEntryDetails(entryId) {
  try {
    const { data } = await client.query({
      query: GET_ENTRY_DETAILS,
      variables: { id: entryId },
    });
    console.log(entryId);
    console.log(data.entries);
    console.log("Entries:", JSON.stringify(data.entries, null, 2));
    return data.entries;
  } catch (error) {
    console.error("Error fetching entry details:", error);
  }
}
