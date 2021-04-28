#!/bin/bash
set -ex

if [ ! -f $DESTDIR/usr/local/lib/libz.a ]; then
    pushd zlib
    ./configure && make -j install DESTDIR=$DESTDIR
    popd
fi

if [ ! -f $DESTDIR/usr/local/lib/libjpeg.a ]; then
    pushd jpeg
    ./configure && make -j install DESTDIR=$DESTDIR
    popd
fi

if [ ! -f $DESTDIR/usr/local/lib/libqpdf.a ]; then
    pushd qpdf
    patch -p1 --ignore-whitespace --unified << 'INSTALL_LIBS'
diff --git a/make/libtool.mk b/make/libtool.mk
index a259afe0..6b4276b3 100644
--- a/make/libtool.mk
+++ b/make/libtool.mk
@@ -106,6 +106,17 @@ endef

 # Install target

+install-libs: build_libqpdf
+	./mkinstalldirs -m 0755 $(DESTDIR)$(libdir)/pkgconfig
+	./mkinstalldirs -m 0755 $(DESTDIR)$(includedir)/qpdf
+	$(LIBTOOL) --mode=install ./install-sh \
+		libqpdf/$(OUTPUT_DIR)/libqpdf.la \
+		$(DESTDIR)$(libdir)/libqpdf.la
+	$(LIBTOOL) --finish $(DESTDIR)$(libdir)
+	./install-sh -m 0644 include/qpdf/*.h $(DESTDIR)$(includedir)/qpdf
+	./install-sh -m 0644 include/qpdf/*.hh $(DESTDIR)$(includedir)/qpdf
+	./install-sh -m 0644 libqpdf.pc $(DESTDIR)$(libdir)/pkgconfig
+
 # NOTE: If installing any new executables, remember to update the
 # lambda layer code in build-scripts/build-appimage.
 install: all
+
INSTALL_LIBS

    ./configure \
        --disable-oss-fuzz \
        --disable-doc-maintenance \
        --disable-html-doc --disable-pdf-doc --disable-validate-doc \
    && make install-libs DESTDIR=$DESTDIR
    find $DESTDIR/usr/local/lib -name 'libqpdf.so*' -type f -exec strip --strip-debug {} \+
    popd
fi
