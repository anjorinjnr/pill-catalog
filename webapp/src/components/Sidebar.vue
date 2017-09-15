<template>
    <aside class="sidebar">
        <div class="scrollbar-inner">
            <div class="user">
                <div class="user__info" data-toggle="dropdown">
                    <img class="user__img" src="demo/img/profile-pics/8.jpg" alt="">
                    <div>
                        <div class="user__name">Tola Anjoriny</div>
                        <div class="user__email">tola@pharma.ng</div>
                    </div>
                </div>

                <div class="dropdown-menu">
                    <a class="dropdown-item" href="">View Profile</a>
                    <a class="dropdown-item" href="">Settings</a>
                    <a class="dropdown-item" href="">Logout</a>
                </div>
            </div>

            <ul class="navigation">
                <!-- <router-link tag="li"
                             active-class="navigation__active"
                             to="/">
                    <a>
                        <i class="zmdi zmdi-home"></i> Home</a>
                </router-link> -->
                <li class="navigation__sub" v-toggle-menu>
                    <a href="">
                        <i class="zmdi zmdi-view-week"></i> Catalog</a>

                    <ul>
                        <li>
                            <a href="hidden-sidebar.html">Category</a>
                        </li>
                        <router-link tag="li"
                                     active-class="navigation__active"
                                     to="/catalog/drugs">
                            <a>Drugs</a>
                        </router-link>

                    </ul>
                </li>

            </ul>
        </div>
    </aside>
</template>