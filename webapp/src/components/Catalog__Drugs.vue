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
        <table class="table mb-0">
          <thead>
          <tr>
            <th>Drug Name</th>
            <th>Registration Number</th>
            <th>Dosage Form</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="drug in drugs" :key="drug.id">
            <td>
              <router-link :to="'/catalog/drugs/' + drug.id">{{ drug.name }}</router-link>
            </td>
            <td> {{ drug.unique_id }}</td>
            <td> {{ drug.dosage_form }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

  </section>
</template>

<script>

  import {mapState, mapActions, mapGetters, mapMutations} from 'vuex';

  export default {

    computed: {
      ...mapState({
        'drugs': state => state.drugs.all
      }),
    },
    methods: {
      ...mapActions([
        'getDrugs'
      ]),

      addDrug: function () {
        this.$router.push('drugs/new');
      }
    },

    created: function () {
      this.getDrugs();

    }
  }
</script>

<style>

</style>
