<template>
  <section class="content">
    <header class="content__title">
      <h1>DRUGS</h1>
    </header>

    <div class="card">
      <div class="card-header">
        <button type="button" class="btn btn-primary  waves-effect"
                @click="addDrug">Add Drug
        </button>
      </div>
      <div class="card-block">
        <div class="table-responsive">
          <table id="data-table" class="table table-bordered mb-0">
            <thead>
            <tr>
              <th>Drug Name</th>
              <th>Registration Number</th>
              <th>Dosage Form</th>
            </tr>
            </thead>
            <tbody>

            </tbody>
            <tbody>
            <tr v-if="!pageInfo.total">
              <td colspan="3">
                There are no records.
              </td>
            </tr>
            <tr v-for="drug in drugs" :key="drug.id">
              <td>
                <router-link :to="'/catalog/drugs/' + drug.id">{{ drug.name }}</router-link>
              </td>
              <td> {{ drug.unique_id }}</td>
              <td> {{ drug.dosage_form }}</td>
            </tr>
            </tbody>

          </table>
          <div class="dataTables_info" id="data-table_info" role="status" aria-live="polite">
            {{tableSummary }}
          </div>
          <div>
            <nav v-if="pageInfo.total > 0">
              <ul class="pagination  justify-content-center">
                <li class="page-item pagination-prev"
                    :class="{disabled: pageInfo.from == 1}">
                  <a class="page-link" href="javascript:void(0)"
                     @click="getPrevPage"></a>
                </li>
                <li class="page-item pagination-next"
                    :class="{disabled: pageInfo.next == null }">
                  <a class="page-link"
                     @click="getNextPage"
                     href="javascript:void(0)"></a>
                </li>
              </ul>
            </nav>
          </div>
        </div>

      </div>
    </div>

  </section>
</template>

<script>

  import {mapState, mapActions, mapGetters, mapMutations} from 'vuex';

  export default {

    computed: {
      ...mapGetters([
        'pageInfo'
      ]),

      ...mapState({
        'drugs': state => state.drugs.all.data,
      }),

      tableSummary: function () {
        if (this.pageInfo.total > 0) {
          let {from, to, total} = this.pageInfo;
          return `Showing ${from} to ${to} of ${total}.`;
        }
      }
    },
    methods: {
      ...mapActions([
        'getDrugs',
        'getNextPage',
        'getPrevPage',
      ]),

      addDrug: function () {
        this.$router.push('drugs/new');
      },

    },

    created: function () {
      this.getDrugs();
    }
  }
</script>

<style>

</style>
