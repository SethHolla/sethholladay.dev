const gulp = require('gulp');
const csso = require('gulp-csso');
const uglify = require('gulp-uglify');
const concat = require('gulp-concat');
const sass = require('gulp-sass')(require('sass'));
const plumber = require('gulp-plumber');
const cp = require('child_process');
const browserSync = require('browser-sync');

const isWindows = /^win/.test(process.platform);
const jekyllCommand = isWindows ? 'bundle.bat' : 'bundle';

/*
 * Build the Jekyll Site
 * runs a child process in node that runs the jekyll commands
 */
gulp.task('jekyll-build', (done) => {
    return cp.spawn(jekyllCommand, ['exec', 'jekyll', 'build'], {stdio: 'inherit', shell: isWindows}).on('close', done);
});

/*
 * Rebuild Jekyll & reload browserSync
 */
gulp.task('jekyll-rebuild', gulp.series('jekyll-build', (done) => {
    browserSync.reload()
    done();
}));

/*
 * Build the jekyll site and launch browser-sync
 */
gulp.task('browser-sync', gulp.series('jekyll-build', (done) => {
    browserSync({
        port: 4000,
        server: {
            baseDir: '_site'
        }
    })
    done();
}));

/*
* Compile and minify sass
*/
gulp.task('sass', () => {
    return gulp.src('src/styles/**/*.scss')
        .pipe(plumber())
        .pipe(sass({quietDeps: true, silenceDeprecations: ['import', 'global-builtin', 'color-functions', 'slash-div']}))
        .pipe(csso())
        .pipe(gulp.dest('assets/css/'));
});

/*
* Compile fonts
*/
gulp.task('fonts', () => {
    return gulp.src('src/fonts/**/*.{ttf,woff,woff2}', {encoding: false})
        .pipe(plumber())
        .pipe(gulp.dest('assets/fonts/'));
});

/**
 * Compile and minify js
 */
gulp.task('js', () => {
    return gulp.src('src/js/**/*.js')
        .pipe(plumber())
        .pipe(concat('main.js'))
        .pipe(uglify())
        .pipe(gulp.dest('assets/js/'));
});

gulp.task('watch', (done) => {
    gulp.watch('./src/js/**/*.js', {usePolling: true}, gulp.series('js', 'jekyll-rebuild'));
    gulp.watch('./src/styles/**/*.scss', {usePolling: true}, gulp.series('sass', 'jekyll-rebuild'));
    gulp.watch('./src/fonts/**/*.{ttf,woff,woff2}', {usePolling: true}, gulp.series('fonts'));
    gulp.watch(['./*html', './_includes/*html', './_layouts/*.html'], {usePolling: true}, gulp.series('jekyll-rebuild'));
    gulp.watch('./_config.yml', {usePolling: true}, gulp.series('jekyll-rebuild'));
    done();
});

gulp.task('default', gulp.series('js', 'sass', 'fonts', 'browser-sync', 'watch'));

gulp.task('build', gulp.series('js', 'sass', 'fonts'));
