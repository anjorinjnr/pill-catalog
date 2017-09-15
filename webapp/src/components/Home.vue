<template>
          <section class="content">
                <header class="content__title">
                    <h1>Dashboard</h1>
                    <small>Welcome to the unique Material Design admin web app experience!</small>

                    <div class="actions">
                            <a href="" class="actions__item zmdi zmdi-trending-up"></a>
                            <a href="" class="actions__item zmdi zmdi-check-all"></a>

                            <div class="dropdown actions__item">
                                <i data-toggle="dropdown" class="zmdi zmdi-more-vert"></i>
                                <div class="dropdown-menu dropdown-menu-right">
                                    <a href="" class="dropdown-item">Refresh</a>
                                    <a href="" class="dropdown-item">Manage Widgets</a>
                                    <a href="" class="dropdown-item">Settings</a>
                                </div>
                            </div>
                        </div>
                </header>

                 <div class="row quick-stats">
                    <div class="col-sm-6 col-md-3">
                        <div class="quick-stats__item bg-light-blue">
                            <div class="quick-stats__info">
                                <h2>987,459</h2>
                                <small>Total Website Traffics</small>
                            </div>

                            <div class="quick-stats__chart sparkline-bar-stats">6,4,8,6,5,6,7,8,3,5,9,5</div>
                        </div>
                    </div>

                    <div class="col-sm-6 col-md-3">
                        <div class="quick-stats__item bg-amber">
                            <div class="quick-stats__info">
                                <h2>356,785K</h2>
                                <small>Total Website Impressions</small>
                            </div>

                            <div class="quick-stats__chart sparkline-bar-stats">4,7,6,2,5,3,8,6,6,4,8,6</div>
                        </div>
                    </div>

                    <div class="col-sm-6 col-md-3">
                        <div class="quick-stats__item bg-purple">
                            <div class="quick-stats__info">
                                <h2>$58,778</h2>
                                <small>Total Total Sales</small>
                            </div>

                            <div class="quick-stats__chart sparkline-bar-stats">9,4,6,5,6,4,5,7,9,3,6,5</div>
                        </div>
                    </div>

                    <div class="col-sm-6 col-md-3">
                        <div class="quick-stats__item bg-red">
                            <div class="quick-stats__info">
                                <h2>214</h2>
                                <small>Total Support Tickets</small>
                            </div>

                            <div class="quick-stats__chart sparkline-bar-stats">5,6,3,9,7,5,4,6,5,6,4,9</div>
                        </div>
                    </div>
                </div>

          </section>
</template>

<script>
import Counter from 'components/Counter'

export default {
  components: {
    Counter
  }
}
</script>
