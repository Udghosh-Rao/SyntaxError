import algoliasearch from 'algoliasearch'

const appId = import.meta.env.VITE_ALGOLIA_APP_ID || ''
const searchKey = import.meta.env.VITE_ALGOLIA_SEARCH_KEY || ''
const indexName = import.meta.env.VITE_ALGOLIA_INDEX || 'events'

let client = null
let index = null

function getIndex() {
  if (!client && appId && searchKey) {
    client = algoliasearch(appId, searchKey)
    index = client.initIndex(indexName)
  }
  return index
}

/**
 * Search events via Algolia instant search.
 * @param {string} query - Search query string
 * @param {object} filters - Optional filter overrides
 * @returns {Promise<Array>} - Array of event hit objects
 */
export async function searchEvents(query, filters = {}) {
  const idx = getIndex()
  if (!idx) {
    console.warn('Algolia not configured — search disabled')
    return []
  }

  const results = await idx.search(query, {
    hitsPerPage: 20,
    ...filters,
  })
  return results.hits
}

export default { searchEvents }
