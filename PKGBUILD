# Maintainer: Etienne Wodey <wodey at iqo dot uni-hannover dot de>

pkgname=python-aqctl-w1-therm-git
_pkgname=aqctl-w1-therm
pkgver=1
pkgrel=1
pkgdesc="ARTIQ controller for sysfs w1 thermometers"
arch=('any')
url="https://github.com/airwoodix/aqctl-w1-therm"
license=('custom')
depends=('python' 'python-aiofiles' 'python-sipyco')
source=('git://github.com/airwoodix/aqctl-w1-therm')
sha256sums=('SKIP')

pkgver() {
    cd $_pkgname
    python setup.py --version
}

build() {
    cd $_pkgname
    python setup.py build
}

package() {
    cd $_pkgname
    python setup.py install --root=${pkgdir} --optimize=1
}

