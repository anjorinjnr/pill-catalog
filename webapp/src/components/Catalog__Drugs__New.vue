<template>
    <section class="content">
        <header class="content__title">
            <h1>Create New Drug</h1>
        </header>

        <div class="card">
            {{ drug}}
            <!-- <div class="card-header">
               <button type="button" class="btn btn-primary">Add Drug</button>
                <!-- <h2 class="card-title">Basic Example</h2>
                <small class="card-subtitle">Using the most basic table markup, here’s how <code>.table</code> -based tables
                    look in Bootstrap.
                </small>
            </div> -->

            <div class="card-block">
                <!--<div class="card-header">-->
                <!--&lt;!&ndash;<h2 class="card-title">Input group</h2>&ndash;&gt;-->
                <!--&lt;!&ndash;<small class="card-subtitle">&ndash;&gt;-->
                <!--&lt;!&ndash;Easily extend form controls by adding text, buttons, or button groups on either side of textual <code>&#x3C;input&#x3E;</code>s.&ndash;&gt;-->
                <!--&lt;!&ndash;</small>&ndash;&gt;-->
                <!--</div>-->
                <div class="card-block">
                    <div class="row" style="margin-top: 15px">
                        <div class="col-sm-6">
                            <div class="form-group">
                                <button @click="save" class="btn btn-primary">Save</button>
                            </div>
                        </div>
                    </div>
                    <form>
                        <div class="form-group">
                            <label>Drug Name</label>
                            <input type="text" class="form-control" placeholder="Drug Name" v-model="drug.name">
                            <i class="form-group__bar"></i>
                        </div>


                        <div class="form-group">
                            <label>Registration Number</label>
                            <input type="text" class="form-control" placeholder="Unique Number e.g NAFDAC REG No."
                                   v-model="drug.unique_id">
                            <i class="form-group__bar"></i>
                        </div>
                        <div class="row">
                            <div class="col-sm-12 ">
                                <div class="form-group">
                                    <label>Category</label>
                                    <v-select v-model="drug.categories"
                                              :multiple="true"
                                              :options="categories"></v-select>

                                    <!--<select v-model="drug.categories" class="select2" v-select2 multiple>-->
                                    <!--<option value="123">Vitamins</option>-->
                                    <!--<option value="234">Antibiotics</option>-->
                                    <!--</select>-->
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Dosage Form {{ drug.dosage_form }}</label>
                            <v-select v-model="drug.dosage_form"
                                      :options="dosage_forms"></v-select>


                            <!--<select v-model="drug.dosage_form" class="select2" v-select2>-->
                            <!--<option value="tablet">Tablet</option>-->
                            <!--<option value="cream">Cream</option>-->
                            <!--<option value="inject">Injection</option>-->
                            <!--</select>-->
                        </div>
                        <div class="form-group">
                            <label>Pack Size</label>
                            <input v-model="drug.pack_size" type="text" class="form-control" placeholder="Pack Size">
                            <i class="form-group__bar"></i>
                        </div>
                        <div class="form-group">
                            <label>Strength</label>
                            <input v-model="drug.strength" type="text" class="form-control" placeholder="Strength">
                            <i class="form-group__bar"></i>
                        </div>
                        <div class="form-group">
                            <label>Active Ingredients</label>
                            <textarea v-model="drug.active_ingredients" class="form-control" rows="5"
                                      placeholder="Active Ingeredients"></textarea>
                            <i class="form-group__bar"></i>
                        </div>
                        <div class="form-group">
                            <label>Manufacturer</label>
                            <input v-model="drug.manufacturer" type="text" class="form-control"
                                   placeholder="Manufacturer">
                            <i class="form-group__bar"></i>
                        </div>


                    </form>
                </div>
                <div class="card-header">
                    <h2 class="card-title">Images</h2>
                </div>

                <div class="card-block">
                    <form action="/v1/image/upload?type=drug"
                    class="dropzone" id="dropzoneUpload">
                    <input name="drug_id" type="hidden" ng-model="drug.id">
                    </form>


                    <div class="row" style="margin-top: 15px">
                        <div class="col-sm-6">
                            <div class="form-group">
                                <button @click="save" class="btn btn-primary">Save</button>
                            </div>
                        </div>
                    </div>


                </div>

            </div>


        </div>


        <footer class="footer hidden-xs-down">
            <p>© Material Admin Responsive. All rights reserved.</p>

            <ul class="nav footer__nav">
                <a class="nav-link" href="">Homepage</a>

                <a class="nav-link" href="">Company</a>

                <a class="nav-link" href="">Support</a>

                <a class="nav-link" href="">News</a>

                <a class="nav-link" href="">Contacts</a>
            </ul>
        </footer>
    </section>
</template>

<script>
  import Dropzone from 'dropzone';
  import vSelect from "vue-select";
  import {mapActions} from 'vuex';
  import _ from 'lodash';


  const data = {
    drug: {
      name: '',
      unique_id: '',
      categories: null,
      dosage_form: null,
      pack_size: '',
      strength: '',
      active_ingredients: '',
      manufacturer: ''
    },
    dosage_forms: ['Tablet', 'Cream', 'Injection'],
    categories: [
      {
        label: 'Vitamin',
        value: 1
      },
      {
        label: 'Antibiotics',
        value: 2
      }
    ]
  };

  export default {
    components: {vSelect},

    data: function () {
      return data;
    },

    methods: {

      ...mapActions([
        'saveDrug'
      ]),

      save: function () {



        this.saveDrug(this.drug)
         .then(data_ => {
             console.log('resp data:', data_);
             if (data_.id) {
                 this.drug = Object.assign({}, this.drug, data_);

                 //upload images.
                 console.log(this.myDropzone.getQueuedFiles());
                 if (this.myDropzone.getQueuedFiles().length > 0) {
                     console.log('upload image');
                     this.myDropzone.processQueue();
                 }
             } else {
                 // check error
             }
       });

      }
    },
    mounted: function () {

      Dropzone.autoDiscover = false;
      Dropzone.options.dropzoneUpload = {
          autoProcessQueue: false
      }
      this.myDropzone = new Dropzone("form#dropzoneUpload");
    }
  }
</script>

<style>

</style>
