<template>
  <section class="content">
    <div class="card">

      <div class="card-block">
        <div class="card-header">
          <h2 class="card-title" v-if="mode=='new'">New Drug</h2>
          <h2 class="card-title" v-else>Update Drug</h2>
        </div>
        <div class="card-block">
          <form>

            <div class="form-group" :class="{'has-danger': errors.has('drug_name') }">
              <label class="form-control-label">Drug Name</label>
              <input type="text" class="form-control"
                     placeholder="Drug Name"
                     name="drug_name"
                     v-validate="'required'"
                     v-model="drug.name">
              <span v-show="errors.has('drug_name')">Enter drug name.</span>
            </div>


            <div class="form-group" :class="{'has-danger': errors.has('unique_id') }">
              <label class="form-control-label">Registration Number</label>
              <input type="text" class="form-control"
                     placeholder="Unique Number e.g NAFDAC REG No."
                     v-validate="'required'"
                     name="unique_id"
                     v-model="drug.unique_id">
              <span v-show="errors.has('unique_id')">Enter drug registration number.</span>
            </div>

            <div class="row new-category">
              <div class="col-sm-6" v-if="addNewCategory">
                <div class="form-group">
                  <label class="form-control-label">Category</label>
                  <input type="text" class="form-control"
                         v-model="newCategoryName"
                         placeholder="Enter category name">
                </div>

              </div>
              <div class="col-sm-6" v-if="addNewCategory">
                <div class="form-group">

                  <button type="button"
                          @click="addCategory"
                          class="btn btn-success">Save
                  </button>
                  <button @click="addNewCategory=false"
                          class="btn">Cancel
                  </button>
                </div>
              </div>

              <div class="col-sm-12" v-if="!addNewCategory">
                <div class="form-group">
                  <label class="form-control-label">Category</label>
                  <v-select v-model="drugCategories"
                            :multiple="true"
                            :options="categoryOptions"></v-select>
                  <a href="javascript:void(0)" @click="addNewCategory=true">Add New Category</a>

                </div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-control-label">Dosage Form</label>
              <v-select v-model="drug.dosage_form"
                        :options="dosage_forms"></v-select>

            </div>
            <div class="form-group">
              <label class="form-control-label">Pack Size</label>
              <input v-model="drug.pack_size"
                     type="text"
                     class="form-control"
                     placeholder="Pack Size">
              <i class="form-group__bar"></i>
            </div>
            <div class="form-group">
              <label class="form-control-label">Strength</label>
              <input v-model="drug.strength" type="text"
                     class="form-control" placeholder="Strength">
              <i class="form-group__bar"></i>
            </div>
            <div class="form-group">
              <label class="form-control-label">Manufacturer</label>
              <input v-model="drug.manufacturer" type="text"
                     class="form-control"
                     placeholder="Manufacturer">
              <i class="form-group__bar"></i>
            </div>
            <div class="form-group">
              <label class="form-control-label">Active Ingredients</label>
              <textarea v-model="drug.active_ingredients"
                        class="form-control" rows="5"
                        placeholder="Active Ingeredients"></textarea>
              <i class="form-group__bar"></i>
            </div>


            <div class="form-group">
              <label class="form-control-label">Details</label>
              <textarea v-model="drug.details"
                        name="details"
                        class="form-control" rows="5"
                        placeholder="Drug Details"></textarea>
              <i class="form-group__bar"></i>
            </div>

          </form>
        </div>
        <div class="card-header">
          <h2 class="card-title images">Images</h2>

          <div class="row lightbox photos" v-if="drug.images">
            <a href="javaScript:void(0)" class="col-md-2 col-4" v-for="img in drug.images">
              <div class="lightbox__item photos__item">
                <img v-bind:src="'/v1/images' + img" alt="">
              </div>
            </a>
          </div>

        </div>

        <div class="card-block">
          <form
                  class="dropzone" id="dropzoneUpload">
            <input name="drug_id" type="hidden" ng-model="drug.id">
          </form>


          <div class="row" style="margin-top: 15px">
            <div class="col-sm-6">
              <div class="form-group">
                <button @click="save" class="btn btn-primary mb-1">
                  Save
                </button>
              </div>
            </div>
          </div>


        </div>

      </div>


    </div>


  </section>
</template>

<script>

  import {mapState, mapActions, mapGetters, mapMutations} from 'vuex';
  import {UPDATE_DRUG} from '../store/mutation_types';
  import _ from 'lodash';
  import alert from '../services/alert';


  const data = {
    drug: {
      name: '',
      unique_id: '',
      categories: [],
      dosage_form: null,
      pack_size: '',
      strength: '',
      active_ingredients: '',
      manufacturer: ''
    },

    dosage_forms: ['Tablet', 'Cream', 'Injection'],

    newCategoryName: '',
    addNewCategory: false
  };


  export default {
    components: {'vSelect': () => import('vue-select')},

    props: {
      id: Number,
      mode: {
        type: String,
        default: 'new'
      }
    },

    data: function () {
      return data;
    },

    computed: {
      ...mapGetters([
        'drugById'
      ]),

      ...mapState({
        'categories': state => state.drugs.categories
      }),

      drugCategories: {
        get: function () {
          if (this.drug && this.drug.categories) {
            return this.drug.categories.map(category => {
              return {label: category.name, value: category.id};
            });
          } else {
            return [];
          }

        },
        set: function (value) {
        }

      },

      categoryOptions: function () {
        return this.categories.map(category => {
          return {label: category.name, value: category.id};
        });
      }

    },

    methods: {

      ...mapMutations({
        updateDrug: UPDATE_DRUG
      }),

      ...mapActions([
        'saveDrug',
        'saveCategory',
        'getDrugById',
        'getCategories',

      ]),

      addCategory: function () {
        this.drug.categories = this.drug.categories || [];
        if (!_.isEmpty(this.newCategoryName)) {
          let category = this.categories.find(category => category.name_lower ==
            this.newCategoryName.toLowerCase().trim());
          if (category) {
            this.drug.categories.push(category);
          } else {
            this.saveCategory({name: this.newCategoryName})
              .then(category => this.drug.categories.push(category))
              .catch(error => console.log(error));
          }
        }
        this.addNewCategory = false;
      },

      _uploadImages: function () {
        if (this.myDropzone.getQueuedFiles().length > 0) {
          this.myDropzone.processQueue();
        }
      },


      save: function () {

        let _save = () => {
          this.drug.categories = this.drugCategories.map(category => {
            return {name: category.label, id: category.value}
          });

          this.saveDrug(this.drug)
            .then(data_ => {
              if (data_.id) {
                alert.notify('Drug saved');
                this.drug = Object.assign({}, this.drug, data_);
                //upload images
                this.myDropzone.options.url += `&drug_id=${this.drug.id}`;
                this._uploadImages();
              }
            })
            .catch(error => alert.error());
        };
        this.$validator.validateAll().then(result => {
          if (result) {
            _save();
          } else {
            alert.error('Some fields are invalid, please correct.')
          }

        });

      }
    },

    mounted: function () {
      import('dropzone').then(Dropzone => {
        Dropzone.autoDiscover = false;
        Dropzone.options.dropzoneUpload = {
          autoProcessQueue: false
        };
        this.myDropzone = new Dropzone("form#dropzoneUpload", {url: '/v1/image/upload?type=drug'});
        this.myDropzone.on('success', () => {
          this._uploadImages();
        });
      });

    },

    created: function () {
      if (this.id) {
        this.getDrugById(this.id).then((drug) => {
          this.drug = drug;
        });
      }
      this.getCategories();
    }
  }
</script>

<style scoped>
  .card-title.images {
    font-weight: bold;
    color: black;
    font-size: 13px;
  }

  .new-category button {
    margin-top: 30px;
  }
</style>
